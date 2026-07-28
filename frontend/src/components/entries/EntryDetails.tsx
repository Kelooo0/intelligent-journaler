import { useEffect } from "react";
import { useState } from "react";
import { getEntry } from "../../api/entriesApi";
import { useParams } from "react-router";
import type { Entry } from "../../types/entry";
import EntryCard from "./EntryCard";
import { deleteEntry } from "../../api/entriesApi";
import { useNavigate } from "react-router";

type EntryDetailsProps = {
    onError: (message: string) => void;
}
export default function EntryDetails({
    onError
}: EntryDetailsProps) {
    const navigate = useNavigate();
    const { id } = useParams<{ id: string}>();
    const [entry, setEntry] = useState<Entry | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
            async function load_entry() {
                try {
                    setIsLoading(true);
                    onError("");

                    const entry_id = Number(id);
                    const data = await getEntry(entry_id);
                    setEntry(data);
                } catch(error) {
                    onError(
                        error instanceof Error
                        ? error.message
                        : "Failed to fetch entry details."
                    )
                    return;
                } finally {
                    setIsLoading(false);
                }
            }
            load_entry()
        }, []);

    async function handleDelete(id:number) {
        const confirmed = window.confirm("Are you sure you want to delete this entry?");

        if(!confirmed) {
            return;
        }
        try {
            setIsLoading(true);
            onError("");
            await deleteEntry(id);
            navigate("/entries/list", {"state": {"message": "Entry deleted succesfully.", "type": "success"}})
        } catch(error) {
            onError(
                error instanceof Error
                ? error.message
                : "Failed to delete entry."
            );
        } finally {
            setIsLoading(false);
        }

    }

    if(isLoading) {
            return (
                <section>
                    <p>Loading entry details...</p>
                </section>
            )
        }

    return (
        <section>
            {entry && <EntryCard entry={entry} onDelete={handleDelete}/>}
        </section>
    )
}
