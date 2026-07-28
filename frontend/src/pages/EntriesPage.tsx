import { Link } from "react-router";
import EntriesList from "../components/entries/EntriesList";
import { useState } from "react";
import { useLocation } from "react-router";
import Assistant from "../components/assistant/Assistant";
import { useEffect } from "react";
import { useNavigate } from "react-router";
import { getEntries } from "../api/entriesApi";
import type { Entry } from "../types/entry";

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
    const [entries, setEntries] = useState<Entry[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    async function load_entries() {
        try {
            setIsLoading(true);
            setError("");

            const data = await getEntries();
            setEntries(data);
        } catch(error) {
            setError(
                error instanceof Error
                ? error.message
                : "Failed to fetch entries."
            )
            return;
        } finally {
            setIsLoading(false);
        }
    }

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
        void load_entries()
    }, []);

    return (
        <main>
           <section>
                <Link to="/entries/new">Add entry</Link>
           </section>
           <section>
                {message && (<p role={type === "error" ? "alert" : "status"}>{message}</p>)}
                {error && <p role="alert">{error}</p>}
           </section>
          <Assistant onSuccess={load_entries}/>
           <section>
                <EntriesList entries={entries} isLoading={isLoading}/>
           </section>
        </main>
    )
}
