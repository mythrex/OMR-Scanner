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

// capture.js
const capture = require('./capture');
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
	capture();
});
