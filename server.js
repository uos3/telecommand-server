const express = require('express');
const app = express();

const bodyParser = require('body-parser');
// const mysql = require('mysql');

const authMiddleware = require('./middleware/auth');

const commandRoutes = require('./routes/command');
const otherRoutes = require('./routes/other');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// mysql configuration
// const mc = mysql.createConnection({
//     host: 'localhost',
//     user: 'root',
//     password: 'its a secret ;)',
//     database: 'telecommand'
// });
// connect to database
// mc.connect();

// authentication stuff
app.use('/api/*', authMiddleware);

// use the routes defined elsewhere
app.use(commandRoutes);
app.use(otherRoutes);

// listen for requests on port 8080
app.listen(8080, function () {
    console.log('Telecommand server is running on port 8080');
});

// app.get('/names', function (req, res) {
//     mc.query('SELECT * FROM test', function (error, results, fields) {
//         if (error) throw error;
//         return res.send({ error: false, data: results, message: 'Name List.' });
//     });
// });
