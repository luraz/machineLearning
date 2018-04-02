# import os.path
import sys
import tarfile
import ntpath
import os

import numpy as np
from six.moves import urllib
import tensorflow as tf
import argparse

from tensorflow.python.framework import tensor_shape
from tensorflow.python.platform import gfile

MODEL_DIR = "/home/laura/games/tensorflowResults/model"
BOTTLENECK_DIR = "/home/laura/games/tensorflowResults/bottlenecks"
IMAGE_PATH = "/home/laura/work/download/motoc/motoc_0.jpg"





class CreateBottleneck:
    def __init__(self, MODEL_DIR, BOTTLENECK_DIR, IMAGE_PATH ):
        pass
        self.MODEL_DIR = MODEL_DIR
        self.BOTTLENECK_DIR = BOTTLENECK_DIR
        self.IMAGE_PATH = IMAGE_PATH

        self.LABEL = ntpath.basename(os.path.dirname(IMAGE_PATH))
        self.BOTTLENECK_PATH = os.path.join(self.BOTTLENECK_DIR, self.LABEL, ntpath.basename(self.IMAGE_PATH) + ".bottleneck")
        self.FLIP_LEFT_RIGHT = False
        self.RANDOM_CROP = 0
        self.RANDOM_SCALE = 0
        self.RANDOM_BRIGHTNESS = 0
        
        # , , image_data_tensor, decoded_image_tensor, resized_input_tensor, bottleneck_tensor
        # self.sess = sess
        # self.image_data = image_data
        # self.jpeg_data_tensor = jpeg_data_tensor
        # self.decoded_image_tensor = decoded_image_tensor
        # self.resized_input_tensor = resized_input_tensor
        # self.bottleneck_tensor = bottleneck_tensor

    def create_model_graph(self, model_info):
        with tf.Graph().as_default() as graph:
            model_path = os.path.join(self.MODEL_DIR, model_info['model_file_name'])
            with gfile.FastGFile(model_path, 'rb') as f:
              graph_def = tf.GraphDef()
              graph_def.ParseFromString(f.read())
              bottleneck_tensor, resized_input_tensor = (tf.import_graph_def(
                  graph_def,
                  name='',
                  return_elements=[
                      model_info['bottleneck_tensor_name'],
                      model_info['resized_input_tensor_name'],
                  ]))
        return graph, bottleneck_tensor, resized_input_tensor

    def run_bottleneck_on_image(self, sess, image_data, image_data_tensor, decoded_image_tensor, resized_input_tensor, bottleneck_tensor):
        resized_input_values = sess.run(decoded_image_tensor,{image_data_tensor: image_data})
        bottleneck_values = sess.run(bottleneck_tensor,{resized_input_tensor: resized_input_values})
        bottleneck_values = np.squeeze(bottleneck_values)
        return bottleneck_values

    def create_bottleneck_file(self, sess, jpeg_data_tensor,decoded_image_tensor, resized_input_tensor, bottleneck_tensor):
        print('Creating bottleneck at ' + self.BOTTLENECK_PATH)
        if not os.path.exists(self.IMAGE_PATH):
            print('File does not exist %s', self.IMAGE_PATH)
            return None
        image_data = gfile.FastGFile(self.IMAGE_PATH, 'rb').read()
        try:
            bottleneck_values = self.run_bottleneck_on_image(sess, image_data, jpeg_data_tensor, decoded_image_tensor,resized_input_tensor, bottleneck_tensor)
        except Exception as e:
            raise RuntimeError('Error during processing file %s (%s)' % (self.IMAGE_PATH, str(e)))
        bottleneck_string = ','.join(str(x) for x in bottleneck_values)
        with open(self.BOTTLENECK_PATH, 'w') as bottleneck_file:
            bottleneck_file.write(bottleneck_string)

    def ensure_dir_exists(self, dir_name):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    def get_or_create_bottleneck(self, sess, jpeg_data_tensor, decoded_image_tensor, resized_input_tensor, bottleneck_tensor):
        self.ensure_dir_exists(os.path.join(self.BOTTLENECK_DIR, self.LABEL))            
        if not os.path.isfile(self.BOTTLENECK_PATH):
            self.create_bottleneck_file(sess, jpeg_data_tensor, decoded_image_tensor, resized_input_tensor, bottleneck_tensor)
        with open(self.BOTTLENECK_PATH, 'r') as bottleneck_file:
            bottleneck_string = bottleneck_file.read()
        did_hit_error = False
        try:
            bottleneck_values = [float(x) for x in bottleneck_string.split(',')]
        except ValueError:
            print('Invalid float found, recreating bottleneck')
            did_hit_error = True
        if did_hit_error:
            self.create_bottleneck_file(sess, jpeg_data_tensor,decoded_image_tensor, resized_input_tensor,bottleneck_tensor)
            with open(self.BOTTLENECK_PATH, 'r') as bottleneck_file:
                bottleneck_string = bottleneck_file.read()
            bottleneck_values = [float(x) for x in bottleneck_string.split(',')]
        return bottleneck_values

    def add_jpeg_decoding(self, input_width, input_height, input_depth, input_mean,input_std):
        jpeg_data = tf.placeholder(tf.string, name='DecodeJPGInput')
        decoded_image = tf.image.decode_jpeg(jpeg_data, channels=input_depth)
        decoded_image_as_float = tf.cast(decoded_image, dtype=tf.float32)
        decoded_image_4d = tf.expand_dims(decoded_image_as_float, 0)
        resize_shape = tf.stack([input_height, input_width])
        resize_shape_as_int = tf.cast(resize_shape, dtype=tf.int32)
        resized_image = tf.image.resize_bilinear(decoded_image_4d,resize_shape_as_int)
        offset_image = tf.subtract(resized_image, input_mean)
        mul_image = tf.multiply(offset_image, 1.0 / input_std)
        return jpeg_data, mul_image

    def should_distort_images(self):
        return (self.FLIP_LEFT_RIGHT or (self.RANDOM_CROP != 0) or (self.RANDOM_SCALE != 0) or (self.RANDOM_BRIGHTNESS != 0))

    def add_input_distortions(self, input_width, input_height,input_depth, input_mean, input_std):
        jpeg_data = tf.placeholder(tf.string, name='DistortJPGInput')
        decoded_image = tf.image.decode_jpeg(jpeg_data, channels=input_depth)
        decoded_image_as_float = tf.cast(decoded_image, dtype=tf.float32)
        decoded_image_4d = tf.expand_dims(decoded_image_as_float, 0)
        margin_scale = 1.0 + (self.RANDOM_CROP / 100.0)
        resize_scale = 1.0 + (self.RANDOM_SCALE / 100.0)
        margin_scale_value = tf.constant(margin_scale)
        resize_scale_value = tf.random_uniform(tensor_shape.scalar(),minval=1.0,maxval=resize_scale)
        scale_value = tf.multiply(margin_scale_value, resize_scale_value)
        precrop_width = tf.multiply(scale_value, input_width)
        precrop_height = tf.multiply(scale_value, input_height)
        precrop_shape = tf.stack([precrop_height, precrop_width])
        precrop_shape_as_int = tf.cast(precrop_shape, dtype=tf.int32)
        precropped_image = tf.image.resize_bilinear(decoded_image_4d,precrop_shape_as_int)
        precropped_image_3d = tf.squeeze(precropped_image, squeeze_dims=[0])
        cropped_image = tf.RANDOM_CROP(precropped_image_3d,[input_height, input_width, input_depth])
        if self.FLIP_LEFT_RIGHT:
            flipped_image = tf.image.random_FLIP_LEFT_RIGHT(cropped_image)
        else:
            flipped_image = cropped_image
        brightness_min = 1.0 - (self.RANDOM_BRIGHTNESS / 100.0)
        brightness_max = 1.0 + (self.RANDOM_BRIGHTNESS / 100.0)
        brightness_value = tf.random_uniform(tensor_shape.scalar(),minval=brightness_min,maxval=brightness_max)
        brightened_image = tf.multiply(flipped_image, brightness_value)
        offset_image = tf.subtract(brightened_image, input_mean)
        mul_image = tf.multiply(offset_image, 1.0 / input_std)
        distort_result = tf.expand_dims(mul_image, 0, name='DistortResult')
        return jpeg_data, distort_result

    def cache_bottlenecks(self, sess, jpeg_data_tensor, decoded_image_tensor,resized_input_tensor, bottleneck_tensor):
        self.ensure_dir_exists(self.BOTTLENECK_DIR)
        self.get_or_create_bottleneck(sess,jpeg_data_tensor, decoded_image_tensor,resized_input_tensor, bottleneck_tensor)
        print ("Bottleneck created")

    def create_model_info(self, architecture):
        architecture = architecture.lower()
        if architecture == 'inception_v3':
            data_url = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'
            bottleneck_tensor_name = 'pool_3/_reshape:0'
            bottleneck_tensor_size = 2048
            input_width = 299
            input_height = 299
            input_depth = 3
            resized_input_tensor_name = 'Mul:0'
            model_file_name = 'classify_image_graph_def.pb'
            input_mean = 128
            input_std = 128
        elif architecture.startswith('mobilenet_'):
            parts = architecture.split('_')
            if len(parts) != 3 and len(parts) != 4:
                tf.logging.error("Couldn't understand architecture name '%s'", architecture)
                return None
            version_string = parts[1]
            if (version_string != '1.0' and version_string != '0.75' and version_string != '0.50' and version_string != '0.25'):
                tf.logging.error(""""The Mobilenet version should be '1.0', '0.75', '0.50', or '0.25', but found '%s' for architecture '%s'""",version_string, architecture)
                return None
            size_string = parts[2]
            if (size_string != '224' and size_string != '192' and size_string != '160' and size_string != '128'):
                tf.logging.error("""The Mobilenet input size should be '224', '192', '160', or '128',but found '%s' for architecture '%s'""",size_string, architecture)
                return None
            if len(parts) == 3:
                is_quantized = False
            else:
                if parts[3] != 'quantized':
                    tf.logging.error("Couldn't understand architecture suffix '%s' for '%s'", parts[3],architecture)
                    return None
                is_quantized = True
            data_url = 'http://download.tensorflow.org/models/mobilenet_v1_'
            data_url += version_string + '_' + size_string + '_frozen.tgz'
            bottleneck_tensor_name = 'MobilenetV1/Predictions/Reshape:0'
            bottleneck_tensor_size = 1001
            input_width = int(size_string)
            input_height = int(size_string)
            input_depth = 3
            resized_input_tensor_name = 'input:0'
            if is_quantized:
                model_base_name = 'quantized_graph.pb'
            else:
                model_base_name = 'frozen_graph.pb'
            model_dir_name = 'mobilenet_v1_' + version_string + '_' + size_string
            model_file_name = os.path.join(model_dir_name, model_base_name)
            input_mean = 127.5
            input_std = 127.5
        else:
            tf.logging.error("Couldn't understand architecture name '%s'", architecture)
            raise ValueError('Unknown architecture', architecture)

        return {
          'data_url': data_url,
          'bottleneck_tensor_name': bottleneck_tensor_name,
          'bottleneck_tensor_size': bottleneck_tensor_size,
          'input_width': input_width,
          'input_height': input_height,
          'input_depth': input_depth,
          'resized_input_tensor_name': resized_input_tensor_name,
          'model_file_name': model_file_name,
          'input_mean': input_mean,
          'input_std': input_std,
        }

    def maybe_download_and_extract(self,data_url):
        dest_directory = self.MODEL_DIR
        if not os.path.exists(dest_directory):
            os.makedirs(dest_directory)
        filename = data_url.split('/')[-1]
        filepath = os.path.join(dest_directory, filename)
        if not os.path.exists(filepath):
            def _progress(count, block_size, total_size):
                sys.stdout.write('\r>> Downloading %s %.1f%%' % (filename, float(count * block_size) / float(total_size) * 100.0))
                sys.stdout.flush()
            filepath, _ = urllib.request.urlretrieve(data_url, filepath, _progress)
            print()
            statinfo = os.stat(filepath)
            tf.logging.info('Successfully downloaded', filename, statinfo.st_size,'bytes.')
        tarfile.open(filepath, 'r:gz').extractall(dest_directory)

def main(argv):
    MODEL_DIR = "/home/laura/games/tensorflowResults/model"
    BOTTLENECK_DIR = "/home/laura/games/tensorflowResults/bottlenecks"
    IMAGE_PATH = "/home/laura/work/download/motoc/motoc_0.jpg"
    ARCHITECTURE = "inception_v3"
    # if len(argv) == 4:
    MODEL_DIR = argv[1]
    BOTTLENECK_DIR = argv[2]
    IMAGE_PATH = argv[3]

    bottleneck = CreateBottleneck(MODEL_DIR, BOTTLENECK_DIR, IMAGE_PATH)
    model_info = bottleneck.create_model_info(ARCHITECTURE)
    bottleneck.maybe_download_and_extract(model_info['data_url'])
    if not model_info:
        print('Did not recognize architecture flag')
        return -1
    do_distort_images = bottleneck.should_distort_images()
    graph, bottleneck_tensor, resized_image_tensor = (bottleneck.create_model_graph(model_info))
    with tf.Session(graph=graph) as sess:
        jpeg_data_tensor, decoded_image_tensor = bottleneck.add_jpeg_decoding(model_info['input_width'], model_info['input_height'], model_info['input_depth'], model_info['input_mean'], model_info['input_std'])
        if do_distort_images:
            (distorted_jpeg_data_tensor, distorted_image_tensor) = bottleneck.add_input_distortions(model_info['input_width'], model_info['input_height'], model_info['input_depth'], model_info['input_mean'], model_info['input_std'])
        else:
            bottleneck.cache_bottlenecks(sess, jpeg_data_tensor,decoded_image_tensor, resized_image_tensor,bottleneck_tensor)
           
if __name__ == '__main__':
    main(sys.argv)