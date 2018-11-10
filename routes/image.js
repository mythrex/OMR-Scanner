var express = require('express');
var router = express.Router();
var multer = require('multer');

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
/* POST users listing. */
router.post('/', upload.single('avatar'), function(req, res, next) {
	console.log(
		'Now fork the python process and call it with arguments grader.py i=' +
			req.file.path
	);
	res.send('respond with a resource');
});

module.exports = router;
