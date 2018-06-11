// $('#plyerlink').click(function()
$(function() {
	$("#plyerlink").click(function(){
	console.log('here1');
       threeDModel();
 });
});

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

	container = document.createElement('div');
	document.body.appendChild(container);
	var lengthLatura = Math.random();
	// camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 10000 );
	var radius = lengthLatura;
	var aspect = window.innerWidth / window.innerHeight;
	camera = new THREE.PerspectiveCamera( 45, aspect, 1, 10000 );
	camera.position.set( 0.0, radius, radius * 3.5 );
	// camera.position.z = 100;
	// camera.position.set( 0.0, radius, radius * 3.5 );
	// scene = new THREE.Scene();
	// renderer = new THREE.WebGLRenderer( { antialias: true } );
		// renderer.setPixelRatio( window.devicePixelRatio );
			// renderer.setSize( window.innerWidth, window.innerHeight );

	renderer = new THREE.CanvasRenderer();	
	renderer.setPixelRatio( window.devicePixelRatio );
	renderer.setSize( window.innerWidth, window.innerHeight );
	container.appendChild( renderer.domElement );

	controls = new THREE.OrbitControls( camera, renderer.domElement );
    // controls.rotateSpeed = 2;
    controls.zoomSpeed = 2;
    // controls.panSpeed = 3;
    controls.enableZoom = true;
    // controls.noPan = false;
    // controls.enableDamping = true;
    // controls.dampingFactor = 0.3;
    // controls.maxPolarAngle = Math.PI/2.0;
    controls.target.set( 0, radius, 0 );
    controls.update();
    drawPatrat(Math.random(), Math.random(), Math.random(), lengthLatura);
	// particles
	// var PI2 = Math.PI * 2;

	// var material = new THREE.SpriteCanvasMaterial( {
	// 	color: 0xffffff,
	// 	program: function ( context ) {
	// 		context.beginPath();
	// 		context.arc( 0, 0, 0.5, 0, PI2, true );
	// 		context.fill();
	// 	}
	// } );

	// var geometry = new THREE.Geometry();
	// for ( var i = 0; i < 100; i ++ ) {
	// 	particle = new THREE.Sprite( material );
	// 	particle.position.x = Math.random() * 2 - 1;
	// 	particle.position.y = Math.random() * 2 - 1;
	// 	particle.position.z = Math.random() * 2 - 1;
	// 	particle.position.normalize();
	// 	particle.position.multiplyScalar( Math.random() * 10 + 450 );
	// 	particle.scale.x = particle.scale.y = 10;
	// 	scene.add( particle );
	// 	geometry.vertices.push( particle.position );
	// }
	// var cont = 1;
	// var diff = 0;


	// var diff = new Array(0, -1 , 1, -2, 2);
	// for (var j = 0; j <5; j ++){
	// var midParticle = null;
	// var geometry = new THREE.Geometry();
	// for (var i = 0; i< 5; i ++){
		
	// 	console.log(diff[j]);
	// 	particle = new THREE.Sprite(material);


	// 	particle.position.x = Math.random()  + diff[j]/2;
	// 	particle.position.y = Math.random()  + diff[j]/2;
	// 	particle.position.z = Math.random()  + diff[j]/2;
	// 	particle.position.normalize();
	// 	particle.position.multiplyScalar( Math.random() * 10 + 350 );

	// 	particle.scale.x = particle.scale.y = 10;
	// 	scene.add( particle );
	// 	geometry.vertices.push( particle.position );
	// 	if (i == 1){
	// 		console.log("equal");
	// 		midParticle = particle;
	// 	}
	// 	if (midParticle != null){
	// 		console.log("not null");
	// 		geometry.vertices.push(midParticle.position);
	// 	}
		
	// 	objects.push(particle);

	// }


	// diff = -diff;
	// diff = diff + 1; 
	// geometry.center();
	// geometry.computeBoundingSphere();

	// var midParticle = null;
	// var geometry2 = new THREE.Geometry();
	// for (var i = 0; i< 5; i ++){
	// 	particle = new THREE.Sprite(material);

	// 	particle.position.x = Math.random() * 2 + 1;
	// 	particle.position.y = Math.random() * 2 + 1;
	// 	particle.position.z = Math.random() * 2 + 1;
	// 	// particle.position.normalize();
	// 	particle.position.multiplyScalar( Math.random() * 10 + 50 );
	// 	// particle.text("sdfsdf");	
	// 	particle.scale.x = particle.scale.y = 10;
	// 	scene.add( particle );
	// 	geometry2.vertices.push( particle.position );
	// 	if (i == 1){
	// 		console.log("equal");
	// 		midParticle = particle;
	// 	}
	// 	if (midParticle != null){
	// 		console.log("not null");
	// 		geometry2.vertices.push(midParticle.position);
	// 	}
		

	// }
	// // geometry2.center();
	// // geometry2.computeBoundingSphere();
	// var line2 = new THREE.Line( geometry2, new THREE.LineBasicMaterial( { color: 0xffffff, opacity: 0.5 } ) );
	// scene.add( line2 );
	// lines
	// var line = new THREE.Line( geometry, new THREE.LineBasicMaterial( { color: 0xffffff, opacity: 0.5 } ) );
	// scene.add( line );

	
// }

	// document.addEventListener( 'mousemove', onDocumentMouseMove, false );
	// document.addEventListener( 'mousemove', onDocumentMouseUp, false );
	// document.addEventListener( 'touchstart', onDocumentTouchStart, false );
	// document.addEventListener( 'touchmove', onDocumentTouchMove, false );
	// window.addEventListener( 'resize', onWindowResize, false );
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
	particle.position.multiplyScalar( Math.random() * 10 + 350 );
	scene.add( particle );
	geometry.vertices.push( particle.position );

	particle2 = new THREE.Sprite(material);
	particle2.position.x = x+l;
	particle2.position.y = y;
	particle2.position.z = z;
	particle2.rotation.y = - 135 * Math.PI / 180;
	// particle2.position.normalize();
	particle2.position.multiplyScalar(Math.random() * 10 + 350 );
	scene.add(particle2);
	geometry.vertices.push(particle2.position);

	particle3 = new THREE.Sprite(material);
	particle3.position.x = x+l;
	particle3.position.y = y-l;
	particle3.position.z = z;
	particle3.rotation.y = - 135 * Math.PI / 180;
	// particle3.position.normalize();
	particle3.position.multiplyScalar(Math.random() * 10 + 350 );
	scene.add(particle3);
	geometry.vertices.push(particle3.position);

	particle4 = new THREE.Sprite(material);
	particle4.position.x = x;
	particle4.position.y = y-l;
	particle4.position.z = z;
	particle4.rotation.y = - 135 * Math.PI / 180;
	// particle4.position.normalize();
	particle4.position.multiplyScalar(Math.random() * 10 + 350 );
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
	particle5.position.multiplyScalar(Math.random() * 10 + 350 );
	scene.add(particle5);
	geometry.vertices.push(particle5.position);
	// geometry.vertices.push(particle8.position);
	// geometry.vertices.push(particle5.position);

	particle6 = new THREE.Sprite(material);
	particle6.position.x = x+l;
	particle6.position.y = y-l;
	particle6.position.z = z+l;
	particle6.rotation.y = - 135 * Math.PI / 180;
	// particle4.position.normalize();
	particle6.position.multiplyScalar(Math.random() * 10 + 350 );
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
	particle7.position.multiplyScalar(Math.random() * 10 + 350 );
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
	particle8.position.multiplyScalar(Math.random() * 10 + 350 );
	scene.add(particle8);
	geometry.vertices.push(particle8.position);
	geometry.vertices.push(particle.position);
	geometry.vertices.push(particle8.position);
	geometry.vertices.push(particle5.position);

	objects.push(particle5);
	objects.push(particle6);
	objects.push(particle7);
	objects.push(particle8);

	var line = new THREE.Line( geometry, new THREE.LineBasicMaterial( { color: 0xffffff, opacity: 0.5 } ) );
	scene.add( line );
	

}

function onWindowResize() {
	windowHalfX = window.innerWidth / 2;
	windowHalfY = window.innerHeight / 2;
	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();
	renderer.setSize( window.innerWidth, window.innerHeight );
}

function onDocumentMouseMove( event ) {
    event.preventDefault();
	var mouse = new THREE.Vector2();
    mouse.x = ( event.clientX / window.innerWidth ) * 2 - 1;
    mouse.y = - ( event.clientY / window.innerHeight ) * 2 + 1;
    raycaster.setFromCamera( mouse, camera );
    if ( SELECTED ) {
        var intersects = raycaster.intersectObject( plane );

        if ( intersects.length > 0 ) {
            SELECTED.position.copy( intersects[ 0 ].point.sub( offset ) );
        }
        return;
    }
    var intersects = raycaster.intersectObjects( objects );
    if ( intersects.length > 0 ) {
        if ( INTERSECTED != intersects[ 0 ].object ) {
            if ( INTERSECTED ) INTERSECTED.material.color.setHex( INTERSECTED.currentHex );
            INTERSECTED = intersects[ 0 ].object;
            INTERSECTED.currentHex = INTERSECTED.material.color.getHex();
            plane.position.copy( INTERSECTED.position );
        }
        container.style.cursor = 'pointer';
    } else {
        if ( INTERSECTED ) INTERSECTED.material.color.setHex( INTERSECTED.currentHex );
        INTERSECTED = null;
        container.style.cursor = 'auto';
    }
}

function onDocumentMouseUp( event ) {
    event.preventDefault();
    controls.enabled = true;

    if ( INTERSECTED ) {
        plane.position.copy( INTERSECTED.position );
        SELECTED = null;

    }
    container.style.cursor = 'auto';
}


function onDocumentTouchStart( event ) {
	if ( event.touches.length > 1 ) {
		event.preventDefault();
		mouseX = event.touches[ 0 ].pageX - windowHalfX;
		mouseY = event.touches[ 0 ].pageY - windowHalfY;
	}
}
function onDocumentTouchMove( event ) {
	if ( event.touches.length == 1 ) {
		event.preventDefault();
		mouseX = event.touches[ 0 ].pageX - windowHalfX;
		mouseY = event.touches[ 0 ].pageY - windowHalfY;
	}
}
//
function animate() {
	requestAnimationFrame( animate );
	render();
}
function render() {
	camera.position.x += ( mouseX - camera.position.x ) * .05;
	camera.position.y += ( - mouseY + 200 - camera.position.y ) * .05;
	camera.lookAt( scene.position );
	renderer.render( scene, camera );
}

}