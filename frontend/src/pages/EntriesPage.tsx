import { Link } from "react-router";
import EntriesList from "../components/entries/EntriesList";
import { useState } from "react";
import { useLocation } from "react-router";
import Assistant from "../components/assistant/Assistant";
import { useEffect } from "react";
import { useNavigate } from "react-router";

interface LocationState {
    message?: string;
    type?: "success" | "error" | "info";
}

export default function EntriesPage() {
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
        <main>
           <section>
                <Link to="/entries/new">Add entry</Link>
           </section>
           <section>
                {message && (<p role={type === "error" ? "alert" : "status"}>{message}</p>)}
                {error && <p role="alert">{error}</p>}
           </section>
          <Assistant />
           <section>
                <EntriesList onError={setError} />
           </section>
        </main>
    )
}
