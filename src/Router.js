import { BrowserRouter,Routes, Route } from "react-router-dom";
import Home from 'routes/Home.js';
import Auth from 'routes/Auth.js';
import Profile from 'routes/Profile.js';
import Navigation from 'components/Navigation.js';

const AppRouter = () => {
    return (
        <BrowserRouter>
            <Navigation/>
            <Routes>
                <Route exact path='/' element={<Home />} />
                <Route path='/auth' element={<Auth />} />
                <Route path='/profile' element={<Profile />} />
            </Routes>
        </BrowserRouter>
    );
};

export default AppRouter;
