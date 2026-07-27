import { useState } from "react"
import EntryDetails from "../components/entries/EntryDetails"
import { useLocation } from "react-router";

interface LocationState {
    message?: string;
    type?: "success" | "error";
}

export default function EntryDetailsPage() {
    const location = useLocation();
    const state = location.state as LocationState | null;
    const [error, setError] = useState("");
    return (
        <main>
            <EntryDetails onError={setError}/>
            <section>
                {state?.message && (<p role={state.type === "error" ? "error" : "status"}>{state.message}</p>)}
                {error && <p role="alert">{error}</p>}
            </section>
        </main>
    )
}
