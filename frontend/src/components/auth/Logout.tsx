import { useNavigate } from "react-router";

export default function LogoutButton() {
    const navigate = useNavigate();

    function handleLogout() {
        localStorage.removeItem("access_token");
        navigate("/home", {"state": {"message": "Logged out succesfully", "type": "success"}})
    }

    return (
        <button onClick={handleLogout}>Logout</button>
    )
}
