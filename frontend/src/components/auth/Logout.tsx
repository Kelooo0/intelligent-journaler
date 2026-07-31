import { useNavigate } from "react-router";
import "../layout/Navbar.css";

export default function LogoutButton() {
    const navigate = useNavigate();

    function handleLogout() {
        localStorage.removeItem("access_token");
        navigate("/", {"state": {"message": "Logged out succesfully.", "type": "success"}})
    }

    return (
        <button onClick={handleLogout} className="navbar-link">Logout</button>
    )
}
