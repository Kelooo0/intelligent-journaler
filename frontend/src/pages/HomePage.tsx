import { Link } from "react-router"
import { useLocation } from "react-router"
import { useNavigate } from "react-router";
import { useEffect } from "react";
import { useState } from "react";

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
        <main>
            <section>
                <h1>Intelligent Journaler</h1>
            </section>
            <section>
                {message && (<p role={type === "error" ? "alert" : "status"}>{message}</p>)}
            </section>
            <section>
                <Link to="/login">Log in</Link>
                <Link to="/register">Register</Link>
            </section>
        </main>
    )
}
