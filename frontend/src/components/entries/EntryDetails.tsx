import { useEffect } from "react";
import { useState } from "react";
import { getEntry } from "../../api/entriesApi";
import { replace, useParams } from "react-router";
import type { Entry } from "../../types/entry";
import EntryCard from "./EntryCard";
import { deleteEntry } from "../../api/entriesApi";
import { useNavigate } from "react-router";
import "../../pages/EntryDetails.css";

type EntryDetailsProps = {
    onError: (message: string) => void;
}
export default function EntryDetails({
    onError
}: EntryDetailsProps) {
    const navigate = useNavigate();
    const [entry, setEntry] = useState<Entry | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const { id } = useParams<{ id: string}>();
    const entry_id = Number(id);

    useEffect(() => {
            async function load_entry() {
                try {
                    setIsLoading(true);
                    onError("");

                    if(!Number.isInteger(entry_id) || entry_id < 0) {
                        navigate("/entries/list", {
                            replace: true, "state": {"message": "Invalid entry ID.", "type": "error"}
                        });

                        return;
                    }
                    const data = await getEntry(entry_id);
                    setEntry(data);
                } catch(error) {
                    const message =
                        error instanceof Error
                        ? error.message
                        : "Failed to fetch entry details."
                    navigate("/entries/list", {
                        replace: true, "state": {"message": message, "type": "error"}
                    });
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
                <h1 className="entry-details-loading">Loading entry details...</h1>
            )
        }

    return (
        <>
            {entry && <EntryCard entry={entry} onDelete={handleDelete}/>}
        </>

    )
}
