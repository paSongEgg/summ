import React from 'react';
import AppRouter from './Router.js';
import Navigation from './components/Navigation.js';

function App() {
    return (
        <div className="App">
            <Navigation/>
            <AppRouter />
        </div>
    )
}

export default App;
