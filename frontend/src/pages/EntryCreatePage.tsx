import EntryForm from "../components/entries/EntryForm";
import { useState } from "react"


export default function EntryCreatePage() {
    const operation_type = "create";
    const [error, setError] = useState("");

    return (
        <main>
            <section>
                <EntryForm onError={setError} operation={operation_type} entryId={null}/>
            </section>
            <section>
                {error && <p role="alert">{error}</p>}
            </section>
        </main>
    )
}
