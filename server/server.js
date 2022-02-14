const express = require("express");
const app = express();
const db = require('./config/db');

app.get('/', (req, res) => {
  db.connect(function (err) {
      db.query("SELECTED * FROM user_table", (err, data) => {
          if (!err) res.send({ 
            data: data 
          });
          else res.send(err);
      })
    });
  });

module.exports = app;


