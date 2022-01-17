const express = require("express");
const app = express();
const port = 3001;
const db = require("./config/db");

app.get("/", (req, res) => {
  db.connect(function (err) {
    if (err) throw err;
    console.log("Connected");
    db.query("SELECTED * FROM user_info", (err, data) => {
      if (!err) res.send({ data: data });
      else res.send(err);
    });
  });

  app.get("/test", (req, res) => {
    db.query("SELECT * FROM quizTable", (err, data) => {
      if (!err) res.send({ products: data });
      else res.send(err);
    });
  });

  app.listen(port, () => {
    console.log(`Connect at http://localhost:${port}`);
  });
});

module.exports = app;
