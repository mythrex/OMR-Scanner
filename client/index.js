/* eslint-disable no-unused-vars */
// styles
const importer = require('./styles/importer.sass');
// libraries
const jquery = require('jquery');
window.$ = jquery;

document.addEventListener('DOMContentLoaded', function() {
	var elems = document.querySelectorAll('.modal');
	var instances = M.Modal.init(elems);
});
