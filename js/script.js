
function threeDModel(){

	var mouseX = 0, mouseY = 0,
	windowHalfX = window.innerWidth / 2,
	windowHalfY = window.innerHeight / 2,
	SEPARATION = 200,
	camera, scene, renderer, container, controls;
	var raycaster = new THREE.Raycaster();
	offset = new THREE.Vector3();
	var INTERSECTED, SELECTED;
	var objects = [];
	init();
	animate();

	function init() {
		var  separation = 100, particle;
		// var x = Math.random();
		var x = 0;
		// var y = Math.random();
		var y = 0;
		// var z = Math.random();
		var z = 0;

		container = document.createElement('div');
		document.body.appendChild(container);
		var lengthLatura = Math.random();
		var radius = lengthLatura;
		var aspect = window.innerWidth / window.innerHeight;
		camera = new THREE.PerspectiveCamera( 45, aspect, 1, 10000 );
		camera.position.set(x+radius/2, y + radius/2, z + radius/2);

		renderer = new THREE.CanvasRenderer();	
		renderer.setPixelRatio( window.devicePixelRatio );
		renderer.setSize( window.innerWidth, window.innerHeight );
		container.appendChild( renderer.domElement );

		controls = new THREE.OrbitControls( camera, renderer.domElement );
	    controls.target.set( 0, radius, 0 );
	    controls.update();
	    drawPatrat(x, y, z, lengthLatura);
	}

	function drawPatrat(x, y, z, l) {
		var PI2 = Math.PI * 2;
		scene = new THREE.Scene();
		var geometry = new THREE.Geometry();
		var material = new THREE.SpriteCanvasMaterial( {
			color: 0xffffff,
			program: function ( context ) {
				context.beginPath();
				context.arc( 0, 0, 0.5, 0, PI2, true );
				context.fill();
			}
		} );
		particle = new THREE.Sprite(material);
		particle.position.x = x;
		particle.position.y = y;
		particle.position.z = z;
		particle.rotation.y = - 135 * Math.PI / 180;
		
		// particle.position.normalize();
		particle.position.multiplyScalar( Math.random() * 10 + 200 );
		scene.add( particle );
		geometry.vertices.push( particle.position );

		particle2 = new THREE.Sprite(material);
		particle2.position.x = x+l;
		particle2.position.y = y;
		particle2.position.z = z;
		particle2.rotation.y = - 135 * Math.PI / 180;
		// particle2.position.normalize();
		particle2.position.multiplyScalar(Math.random() * 10 + 200 );
		scene.add(particle2);
		geometry.vertices.push(particle2.position);

		particle3 = new THREE.Sprite(material);
		particle3.position.x = x+l;
		particle3.position.y = y-l;
		particle3.position.z = z;
		particle3.rotation.y = - 135 * Math.PI / 180;
		// particle3.position.normalize();
		particle3.position.multiplyScalar(Math.random() * 10 + 200 );
		scene.add(particle3);
		geometry.vertices.push(particle3.position);

		particle4 = new THREE.Sprite(material);
		particle4.position.x = x;
		particle4.position.y = y-l;
		particle4.position.z = z;
		particle4.rotation.y = - 135 * Math.PI / 180;
		// particle4.position.normalize();
		particle4.position.multiplyScalar(Math.random() * 10 + 200 );
		scene.add(particle4);
		geometry.vertices.push(particle4.position);

		geometry.vertices.push(particle.position);
		geometry.vertices.push(particle4.position);
		objects.push(particle);
		objects.push(particle2);
		objects.push(particle3);
		objects.push(particle4);


		particle5 = new THREE.Sprite(material);
		particle5.position.x = x;
		particle5.position.y = y-l;
		particle5.position.z = z+l;
		particle5.rotation.y = - 135 * Math.PI / 180;
		// particle4.position.normalize();
		particle5.position.multiplyScalar(Math.random() * 10 + 200 );
		scene.add(particle5);
		geometry.vertices.push(particle5.position);

		particle6 = new THREE.Sprite(material);
		particle6.position.x = x+l;
		particle6.position.y = y-l;
		particle6.position.z = z+l;
		particle6.rotation.y = - 135 * Math.PI / 180;
		// particle4.position.normalize();
		particle6.position.multiplyScalar(Math.random() * 10 + 200 );
		scene.add(particle6);
		geometry.vertices.push(particle6.position);
		geometry.vertices.push(particle3.position);
		geometry.vertices.push(particle6.position);

		particle7 = new THREE.Sprite(material);
		particle7.position.x = x+l;
		particle7.position.y = y;
		particle7.position.z = z+l;
		particle7.rotation.y = - 135 * Math.PI / 180;
		// particle4.position.normalize();
		particle7.position.multiplyScalar(Math.random() * 10 + 200 );
		scene.add(particle7);
		geometry.vertices.push(particle7.position);
		geometry.vertices.push(particle2.position);
		geometry.vertices.push(particle7.position);

		particle8 = new THREE.Sprite(material);
		particle8.position.x = x;
		particle8.position.y = y;
		particle8.position.z = z+l;
		particle8.rotation.y = - 135 * Math.PI / 180;
		// particle4.position.normalize();
		particle8.position.multiplyScalar(Math.random() * 10 + 200 );
		scene.add(particle8);
		geometry.vertices.push(particle8.position);
		geometry.vertices.push(particle.position);
		geometry.vertices.push(particle8.position);
		geometry.vertices.push(particle5.position);

		// geometry.translate( (particle8.position.x+x)/2, (particle8.position.y+ y)/2, (particle8.position.z+z)/2 );
		objects.push(particle5);
		objects.push(particle6);
		objects.push(particle7);
		objects.push(particle8);

		var line = new THREE.Line( geometry, new THREE.LineBasicMaterial( { color: 0xffffff, opacity: 0.5 } ) );
		scene.add( line );
	}

	function onWindowResize() {
		camera.aspect = window.innerWidth / window.innerHeight;
		camera.updateProjectionMatrix();
		renderer.setSize( window.innerWidth, window.innerHeight );
		}

	function animate() {
		requestAnimationFrame( animate );
		render();
	}
	function render() {
		camera.lookAt( scene.position );
		renderer.render( scene, camera );
	}
}



$(function() {
  // We can attach the `fileselect` event to all file inputs on the page
  $(document).on('change', ':file', function() {
    var input = $(this),
        numFiles = input.get(0).files ? input.get(0).files.length : 1,
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [numFiles, label]);
  });

  // We can watch for our custom `fileselect` event like this
  $(document).ready( function() {
      $(':file').on('fileselect', function(event, numFiles, label) {

          var input = $(this).parents('.input-group').find(':text'),
              log =  label;

          if( input.length ) {
              input.val(log);
          } 
      });
  });
  
});

// $('#plyerlink').click(function()
$(function() {
	$("#plyerlink").click(function(){
	console.log('here1');
       threeDModel();
 });
});


// $(function() {
// 	$(".nav li a").click(function() {
// 	   $(".nav").find(".active").removeClass("active");
// 	   $(this).parent().addClass("active");
// 	});
// });


//seachPcapBTN
$(function() {
	$("#seachPcapBTN").click(function() {
		var ok = 0;
		// $("input[name='inputdictionary']").each( function () {
			var value = document.getElementById("searchFileInput").value;
			console.log(value);
			if (value.length > 2){
				var key = document.getElementById("searchFileCombobox").value; 
				console.log(key);
			}; 
			// var key = $(this).prop('id');
			// var value = $(this).prop('value');
			// console.log(key); 
			// console.log(value);
			// if (value.length > 0 && value.length < 3){
			// 	dialog("Filter length must be longer");
			// };
			// if (value.length > 2){
			// 	ok = 1;
		// };
		
		// if (ok == 0){
		// 	dialog("No filter");
		// 	};
		// });
	});
});