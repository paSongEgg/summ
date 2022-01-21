import { useState } from "react";

import { Auth } from 'aws-amplify'

import { Container, Col, Button, Form } from "react-bootstrap"


const Authorization = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [newAccount, setNewAccount] = useState(true);

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
        let data;
        if (newAccount) {
            //await createUser
        } else {
            //await signIn
        }
    };
    const loginToCreate = () => setNewAccount((prev) => !prev);
    return (
        <Container fluid>
                <Col sm={4}>
                <form onSubmit={onSubmit}>
                <Form.Group className="mb-3" controlId="formBasicEmail">
                    <Form.Label>Email</Form.Label>
                    <Form.Control 
                        name="email"
                        type="email"
                        placeholder="Email"
                        required
                        value={email}
                        onChange={onChange} />
                </Form.Group>

                <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control 
                    name="password"
                    type="password"
                    placeholder="Password"
                    required
                    value={password}
                    onChange={onChange} />
                </Form.Group>
                <Button 
                    variant="primary" 
                    type="submit"
                    value={newAccount ? "계정생성" : "로그인"}>
                    Submit
                </Button>
            </form>
            <span onClick={loginToCreate}>
                {newAccount ? "로그인" : "계정생성"}
            </span>{' '}
            <Button
                onClick={() => Auth.federatedSignIn({ provider: "Google" })}
                variant="outline-danger">
                    Sign in with Google
            </Button>
            </Col>
        </Container>
    );
};
export default Authorization;