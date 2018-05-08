const mysql = require('mysql');

exports.send_command = function (req, res) {
    const command = req.body.command;

    // verify validity of command
    //  - lovely javascript bitwise operations probably

    // log command (w/ server timestamp)
    //  - myqsl

    // get time of next cubesat pass from orbit prediction thing
    //  - how to call & get the response?

    // get azumith & elevation of next cubesat pass from orbit prediction thing
    //  - how to call & get the response?

    // send data
    //  - how? in what form (binary?)? where to?

    return res.send({ error: false, message: 'command sent!' });
}

exports.most_recent = function (req, res) {
    // return most recent command from db

    return res.send({ error: false, message: 'ain\'t no commands yet' });
}
