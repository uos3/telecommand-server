const express = require('express');
const router = express.Router();

const controller = require('../controllers/command');

router.route('/api/command')
    .get(controller.most_recent)
    .post(controller.send_command);

module.exports = router;
