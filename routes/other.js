const express = require('express');
const router = express.Router();

// default route
router.get('/', function (req, res) {
    return res.send({ error: true, message: 'hello' });
});

module.exports = router;
