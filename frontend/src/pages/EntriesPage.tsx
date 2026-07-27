import { Link } from "react-router";
import EntriesList from "../components/entries/EntriesList";
import { useState } from "react";
import { useLocation } from "react-router";

interface LocationState {
    message?: string;
    type?: "success" | "error";
}

export default function EntriesPage() {
    const location = useLocation();
    const state = location.state as LocationState | null;
    const [error, setError] = useState("");

    return (
        <main>
           <section>
                <Link to="/entries/new">Add entry</Link>
           </section>
           <section>
                {state?.message && (<p role={state.type === "error" ? "error" : "status"}>{state.message}</p>)}
                {error && <p role="error">{error}</p>}
           </section>
           <section>
                <EntriesList onError={setError} />
           </section>
        </main>
    )
}
