import { Link } from "react-router-dom";
const Navigation = () => {
    return (
        <div>
            <Link to="/">Home</Link>
            <Link to="/profile">Profile</Link>
            <Link to="/auth">Auth</Link>
        </div>
    );
};
export default Navigation;