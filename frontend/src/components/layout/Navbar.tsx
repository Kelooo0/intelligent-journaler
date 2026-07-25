import { Link } from "react-router";
import LogoutButton from "../auth/Logout";

export default function Navbar() {
    return (
        <nav>
            <Link to="/entries">Entries</Link>
            <LogoutButton />
        </nav>
    )
}
