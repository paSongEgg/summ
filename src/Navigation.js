import { Link } from "react-router-dom";
const Navigation = () => {
    return (
        <div>
            <Link to="/home">Main</Link>
            <Link to="/slider">slider</Link>
        </div>
    );
};
export default Navigation;