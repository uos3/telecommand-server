const express = require('express');
const router = express.Router();

const controller = require('../controllers/command');

router.route('/api/command')
    .post(controller.send_command);

module.exports = router;
