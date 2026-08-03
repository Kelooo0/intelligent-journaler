import { useState } from "react"
import EntryDetails from "../components/entries/EntryDetails"
import { useLocation } from "react-router";
import { useNavigate } from "react-router";
import { useEffect } from "react";
import "./EntryDetails.css";

interface LocationState {
    message?: string;
    type?: "success" | "error" | "info";
}

export default function EntryDetailsPage() {
    const location = useLocation();
    const navigate = useNavigate();
    const state = location.state as LocationState | null;
    const [error, setError] = useState("");
    const [message, setMessage] = useState(state?.message ?? "");
    const [type, setType] = useState<LocationState["type"]>(state?.type ?? "info");

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

    return (
        <main className="entry-details-main">
            <section className="entry-details-msgs">
                {message && (<p role={type === "error" ? "alert" : "status"}>{message}</p>)}
                {error && <p role="alert">{error}</p>}
            </section>
            <section className="entry-details-container">
                <EntryDetails onError={setError}/>
            </section>
        </main>
    )
}
