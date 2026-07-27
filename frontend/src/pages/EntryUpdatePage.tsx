import EntryForm from "../components/entries/EntryForm";
import { useState } from "react"
import { useParams } from "react-router";

export default function EntryUpdatePage() {
    const operation_type = "update";
    const [error, setError] = useState("");
    const { id } = useParams<{ id: string }>();
    const entry_id = Number(id);

    return (
        <main>
            <section>
                <EntryForm onError={setError} operation={operation_type} entryId={entry_id}/>
            </section>
            <section>
                {error && <p role="alert">{error}</p>}
            </section>
        </main>
    )
}
