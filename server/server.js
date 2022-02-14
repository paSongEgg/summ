const express = require('express');
const app = express();
const path=require('path');
const router=require('routes/Router');
const db = require('server/config/db');
const PORT=db.PORT||4000;
app.use(express.static(path.join(__dirname,'..','public/')));
app.use('/',router);
module.exports = app;

app.listen(PORT,()=>{
    console.log('Check out the app at http://localhost:${PORT}');
});