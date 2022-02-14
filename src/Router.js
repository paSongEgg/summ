import { BrowserRouter,Routes, Route } from "react-router-dom";
import Home from 'routes/Home.js';
import Slider from 'routes/Slider.js';
import Navigation from 'Navigation.js';

const AppRouter = () => {
    return (
        <BrowserRouter>
            <Navigation/>
            <Routes>
                <Route exact path='/' element={<Home />} />
                <Route path='/slider' element={<Slider />} />
            </Routes>
        </BrowserRouter>
    );
};

export default AppRouter;
