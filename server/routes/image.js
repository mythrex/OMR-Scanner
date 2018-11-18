/* eslint-disable no-unused-vars */
/* eslint-disable no-console */
var express = require('express');
var router = express.Router();
var multer = require('multer');
const { spawn } = require('child_process');

// for appending extention
var storage = multer.diskStorage({
	destination: function(req, file, cb) {
		cb(null, 'server/uploads');
	},
	filename: function(req, file, cb) {
		cb(null, Date.now() + '.' + file.originalname.split('.').pop());
	}
});

var upload = multer({ storage: storage });
/* POST Image listing. */
router.post('/', upload.single('avatar'), function(req, res, next) {
	// eslint-disable-next-line no-console
	// console.log(req.file);
	const analyseOmr = spawn('python', [
		'server/bin/module/grader.py',
		'-i',
		req.file.path
	]);

	analyseOmr.stdout.on('data', data => {
		// console.log(`stdout: ${data}`, data);
		var fileName = req.file.path.split('/').pop();
		res.redirect(`/images/${fileName}/0`);
	});

	analyseOmr.stderr.on('data', err => {
		console.log(`stderr: ${err}`);
		res.redirect('/images/1542192346700.jpg/1');
	});

	analyseOmr.on('close', code => {
		console.log(`child process exited with code ${code}`);
	});
});

router.get('/:image/:e', function(req, res, next) {
	var image = req.params.image;
	var e = req.params.e;
	if (!e) {
		res.render('result', {
			original: `/${image}`,
			result: `/result/${image}`,
			production: process.env.NODE_ENV === 'production'
		});
	} else {
		res.render('result', {
			original: '/images/failsafe/1542286342686.jpg',
			result: '/images/failsafe/result/1542286342686.jpg',
			production: process.env.NODE_ENV === 'production'
		});
	}
});
module.exports = router;
