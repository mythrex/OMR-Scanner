var express = require('express');
var router = express.Router();

/* POST users listing. */
router.post('/', function(req, res, next) {
	res.send('respond with a resource');
	// eslint-disable-next-line no-console
	console.log(req.params);
});

module.exports = router;
