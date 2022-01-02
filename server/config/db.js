var mysql = require('mysql');
const db = mysql.createPool({
	host: process.env.REACT_APP_HOST,
	port: process.env.REACT_APP_PORT,
	user: process.env.REACT_APP_USER,
	password: process.env.REACT_APP_PASSWORD,
	database: process.env.REACT_APP_DB
});

module.exports = db;
