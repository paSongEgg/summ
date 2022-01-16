import { useState } from "react";

import { Auth } from 'aws-amplify'

const Authorization = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [newAccount, setNewAccout] = useState(true);

    const onChange = (event) => {
        const {
            target: { name, value },
        } = event;
        if (name === "email") {
            setEmail(value);
        } else if (name === "password") {
            setPassword(value);
        }
    };

    const onSubmit = (event) => {
        event.preventDefault();
    };
    const loginToCreate = () => setNewAccout((prev) => !prev);
    return (
        <div>
            <form onSubmit={onSubmit}>
                <input
                    name="email"
                    type="email"
                    placeholder="Email"
                    required
                    value={email}
                    onChange={onChange}
                />
                <input
                    name="password"
                    type="password"
                    placeholder="Password"
                    required
                    value={password}
                    onChange={onChange}
                />
                <input
                    type="submit"
                    value={newAccount ? "계정생성" : "로그인"}
                />
            </form>
            <span onClick={loginToCreate}>
                {newAccount ? "로그인" : "계정생성"}
            </span>
            <button
            onClick={() => Auth.federatedSignIn({ provider: "Google" })}>
                <img src="img/btn_google_signin_light_normal_web.png" style={{height:"45px", width:"190px"}}/>
            </button>
        </div>
    );
};
export default Authorization;