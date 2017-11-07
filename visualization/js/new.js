/**
 * Created by oles on 16.08.16.
 */

THREE.LineSegments = function ( geometry, material ) {

	THREE.Line.call( this, geometry, material );

	this.type = 'LineSegments';

};

THREE.LineSegments.prototype = Object.assign( Object.create( THREE.Line.prototype ), {

	constructor: THREE.LineSegments

} );

function createGeometry() {

				var geometry = new THREE.Geometry();

				for ( i = 0; i < 1500; i ++ ) {

					var vertex1 = new THREE.Vector3();
					vertex1.x = Math.random() * 2 - 1;
					vertex1.y = Math.random() * 2 - 1;
					vertex1.z = Math.random() * 2 - 1;
					vertex1.normalize();
					vertex1.multiplyScalar( r );

					vertex2 = vertex1.clone();
					vertex2.multiplyScalar( Math.random() * 0.09 + 1 );

					geometry.vertices.push( vertex1 );
					geometry.vertices.push( vertex2 );

				}

				return geometry;

			}

geom = createGeometry()

mat = new THREE.LineBasicMaterial( { color: new THREE.Color( '#00b3ff' ), opacity: 0.7, linewidth: 1 } );

line = new THREE.LineSegments( geom, mat );
line.scale.x = line.scale.y = line.scale.z = 1;
line.originalScale = 1;
line.rotation.y = Math.random() * Math.PI;
line.updateMatrix();

this.meshComponents.add(line)

