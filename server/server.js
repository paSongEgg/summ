const express = require('express');
const app = express();
const PORT = process.env.PORT || 3001;
const db = require('./config/db');

app.get('/api/products', (req, res) => {
    db.query("SELECT * FROM user_info", (err, data) => {
        if (!err) res.send({ products: data });
        else res.send(err);
    })
})

//DB INSERT
let sql = "INSERT INTO user_info (name,email) VALUES(?,?)";
let params = ['test2', 'test2@hanmail.net'];

db.query(sql, params, function (err, rows, fields) {
    if (err) {
        console.log(err);
    }
    else {
        console.log(rows.insertId);
    }
})

app.listen(PORT, () => {
    console.log(`Server On : http://localhost:${PORT}/`);
})