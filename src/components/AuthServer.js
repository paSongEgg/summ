router.post('/onLogin', (req, res) => {
    const userID = req.query.userID;
    const userPW = req.query.userPW;
    const isExist = 'select count(*) as result from user_table where userID=?';
    const signUp = 'insert into user_table (userID,password) values(?,?);';
    db.query(isExist, userID, (err, data) => {
        if (!err) {
            if (data[0] > 0) {
                res.send({ 'msg': '이미 존재하는 이메일입니다.' });
            }
            else {
                db.query(signUp, userID, userPW, (err, data) => {
                    if (!err) {
                        res.send(data[0]);
                    }
                    else {
                        res.send(err);
                    }
                });
            }
        }
        else {
            res.send(err);
        }
    }
});