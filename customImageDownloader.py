import os
from bs4 import BeautifulSoup  #de instalat
import requests # de instalat
import re
import urllib2
import cookielib
import json
import argparse
import sys

class ImageDownloader:
    def __init__(self, keyword, nbImages, downloadPath):
        self.keyword = keyword
        self.nbImages = nbImages
        self.downloadPath = os.path.join(downloadPath, keyword)

        self.prepare()

    def prepare(self):
        if not os.path.isdir(self.downloadPath):
            os.makedirs(self.downloadPath)

    def get_soup(self, url,header):
        return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

    def downloadImages(self):
        query = self.keyword
        image_type = str(self.keyword)
        
        query = query.split()
        query = '+'.join(query)
       
        url = "https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
       
        print url
       
        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        }

        soup = self.get_soup(url,header)
        ActualImages=[]
        
        for a in soup.find_all("div",{"class":"rg_meta"}, limit=self.nbImages):
            linkImage , imgType =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
            ActualImages.append((linkImage,imgType))

        print  "there are total %s images" % str(len(ActualImages))
        counter = 0
        for i , (img , imgType) in enumerate(ActualImages):
            try:
                request = urllib2.Request(img, headers={'User-Agent' : header})
                raw_img = urllib2.urlopen(request).read()

                print counter

                if len(imgType)==0:
                    imgType = "jpg"

                destFile = open(os.path.join(self.downloadPath, image_type + "_"+ str(counter)+"."+imgType), 'wb')
                destFile.write(raw_img)
                destFile.close()
                counter += 1

            except Exception as e:
                print "could not load : %s with exception : %s " % (str(img), str(e))

def main(argv):
    keyword = "smartphone"
    nbImages = 100
    downloadPath = "/home/laura/work/download"

    parser = argparse.ArgumentParser(description="Google SearchImages")
    parser.add_argument("-keyword", type=str, help="Keyword to search for")
    parser.add_argument("-nb", type=int, help="Number of images to download")
    parser.add_argument("-path", type=str, help="Path to download images to")

    args = parser.parse_args(argv[1:])
    if args.keyword:
        keyword = args.keyword
    if args.nb:
        nbImages = args.nb
    if args.path:
        downloadPath = args.path

    if nbImages > 100:
        print "Can't download more than 100 images!!"
        nbImages = 100

    if not os.path.isdir(downloadPath):
        os.makedirs(downloadPath)

    imageDownloader = ImageDownloader(keyword, nbImages, downloadPath)
    imageDownloader.downloadImages()


if __name__ == '__main__':
    main(sys.argv)







