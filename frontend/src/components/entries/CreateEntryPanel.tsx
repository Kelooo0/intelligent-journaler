import CreateEntryForm from "./CreateEntryForm"
import { useState } from "react"

export default function CreateEntryPanel() {
    const [error, setError] = useState("");
    return (
        <section id="create-entry-panel">
            <CreateEntryForm onError={setError}/>
            <section>
                {error && <p role="alert">{error}</p>}
            </section>
        </section>
    )
}
