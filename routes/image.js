/* eslint-disable no-console */
var express = require('express');
var router = express.Router();
var multer = require('multer');
const { spawn } = require('child_process');

// for appending extention
var storage = multer.diskStorage({
	destination: function(req, file, cb) {
		cb(null, 'uploads');
	},
	filename: function(req, file, cb) {
		cb(null, Date.now() + '.' + file.originalname.split('.').pop());
	}
});

var upload = multer({ storage: storage });
/* POST Image listing. */
router.post('/', upload.single('avatar'), function(req, res, next) {
	// eslint-disable-next-line no-console
	const analyseOmr = spawn('python', [
		'bin/module/grader.py',
		'-i',
		req.file.path
	]);

	analyseOmr.stdout.on('data', data => {
		// console.log(`stdout: ${data}`, data);
		var fileName = req.file.path.split('/').pop();
		res.redirect(`/images/${fileName}`);
	});

	analyseOmr.stderr.on('data', err => {
		// console.log(`stderr: ${err}`);
		res.status(404).send(err);
	});

	analyseOmr.on('close', code => {
		console.log(`child process exited with code ${code}`);
	});
});

router.get('/:image', function(req, res, next) {
	var image = req.params.image;
	res.render('result', { original: `/${image}`, result: `/result/${image}` });
});
module.exports = router;
