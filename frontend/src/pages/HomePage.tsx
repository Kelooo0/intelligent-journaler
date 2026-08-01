import { Link } from "react-router"
import { useLocation } from "react-router"
import { useNavigate } from "react-router";
import { useEffect } from "react";
import { useState } from "react";
import "./HomePage.css";

interface LocationState {
    message?: string;
    type?: "success" | "error" | "info";
}

type SavedMessage = {
    message: string;
    type: "success" | "error" | "info";
}

export default function HomePage() {
    const location  = useLocation();
    const navigate = useNavigate();
    const state = location.state as LocationState | null;
    const [message, setMessage] = useState(state?.message ?? "");
    const [type, setType] = useState(state?.type ?? "info");

    useEffect(() => {
        if (state?.message) {
            setMessage(state.message);
            setType(state.type ?? "info");
            navigate(location.pathname, {
                replace: true,
                state: null,
            });
        }
  }, [state?.message, navigate]);

    useEffect(() => {
        const state = sessionStorage.getItem("state");

        if(!state) {
            return;
        }

        const data = JSON.parse(state) as SavedMessage;
        setMessage(data.message);
        setType(data.type);
        sessionStorage.removeItem("state");
    }, []);

    return (
        <main className="home-main">
            <section className="home-header">
                <h2>Welcome to</h2>
                <h1>Intelligent Journaler</h1>
            </section>
            <section className="home-buttons">
                <section className="home-button-box login-box">
                    <Link to="/login" className="home-link login-link">Log in</Link>
                </section>
                 <section className="home-button-box register-box">
                    <Link to="/register" className="home-link register-link">Register</Link>
                </section>
            </section>
            <section className="home-messages">
                {message && (<p role={type === "error" ? "alert" : "status"}>{message}</p>)}
            </section>
        </main>
    )
}
