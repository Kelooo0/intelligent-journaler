import CreateEntryForm from "./CreateEntryForm"
import { useState } from "react";
import type { Entry } from "../../types/entry";
import CreateEntryResult from "./CreateEntryResult";
export default function CreateEntryPanel() {
    const [result, setResult] = useState<Entry | null>(null);
    const [error, setError] = useState("");
    return (
        <section id="create-entry-panel">
            <CreateEntryForm onSuccess={setResult} onError={setError} />

            {error && <p role="alert">{ error }</p>}
            {result && <CreateEntryResult result={ result } />}
        </section>
    )
}
