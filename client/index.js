/* eslint-disable no-undef */
/* eslint-disable no-unused-vars */

// styles
const importer = require('./styles/importer.sass');
// libraries
const jquery = require('jquery');
window.$ = jquery;
// materialize
const materialize = require('materialize-css');
const materializeCss = require('../node_modules/materialize-css/dist/css/materialize.min.css');

document.addEventListener('DOMContentLoaded', function() {
	var elems = document.querySelectorAll('.modal');
	// eslint-disable-next-line no-undef
	var instances = M.Modal.init(elems);
	var carousel = document.querySelectorAll('.carousel');
	var carouselIntance = M.Carousel.init(carousel, {
		fullWidth: true,
		indicators: true,
		duration: 0
	});

	// for displaying image on selection
	function showImage(src, target) {
		var fr = new FileReader();
		// when image is loaded, set the src of the image where you want to display it
		fr.onload = function(e) {
			target.src = this.result;
		};
		src.addEventListener('change', function() {
			// fill fr with image data
			fr.readAsDataURL(src.files[0]);
		});
	}

	var src = document.getElementById('upload-btn');
	var target = document.getElementById('placeholder-img');
	// showImage(src, target);
});
