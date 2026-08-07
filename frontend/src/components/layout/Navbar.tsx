import { Link } from "react-router";
import LogoutButton from "../auth/Logout";
import "./Navbar.css";

export default function Navbar() {
  return (
    <nav className="navbar">
      <section className="navbar-link-box">
        <Link to="/entries/list" className="navbar-link">
          Entries
        </Link>
      </section>
      <section className="navbar-link-box">
        <LogoutButton />
      </section>
    </nav>
  );
}
