import { BrowserRouter,Routes, Route } from "react-router-dom";
import Home from 'routes/SectionNews.js';
import SectionNews from 'routes/Home.js';
import Navigation from 'Navigation.js';
import Floating from "components/Floating";

const AppRouter = () => {
    return (
        <BrowserRouter>
            <Navigation/>
            <Routes>
                <Route exact path='/' element={<Home />} />
                <Route path='/sections' element={<SectionNews />} />
            </Routes>
        </BrowserRouter>
    );
};

export default AppRouter;
