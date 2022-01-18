const mysql = require("mysql");

const db = mysql.createPool({
  host: process.env.REACT_APP_HOST,
  user: process.env.REACT_APP_USER,
  password: process.env.REACT_APP_PASSWORD,
  database: process.env.REACT_APP_DB,
});

module.exports = db;
