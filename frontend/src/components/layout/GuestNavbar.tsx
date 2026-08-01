import { Link } from "react-router";
import "./Navbar.css";

export default function GuestNavbar() {
    return (
        <nav className="navbar">
            <section className="navbar-link-box">
                <Link to="/" className="navbar-link">Home</Link>
            </section>
        </nav>
    )
}
