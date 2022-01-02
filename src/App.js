import React, { Component } from 'react';
import axios from 'axios';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            hello: [],
        }
    }

    componentDidMount() {
        this._getHello();
    }

    _getHello = async () => {
        const res = await axios.get('/hello');
        this.setState({ hello: res.data.hello })
        console.log(this.state.hello);
    }

    render() {
        return (
            <>
                <h3>get DB data(������ ���߸�� �ܼ�Ȯ��)</h3>
            </>
        )
    }
}

export default App;
