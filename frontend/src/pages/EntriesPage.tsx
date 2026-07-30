import { Link } from "react-router";
import EntriesList from "../components/entries/EntriesList";
import { useState } from "react";
import { useLocation } from "react-router";
import Assistant from "../components/assistant/Assistant";
import { useEffect } from "react";
import { useNavigate } from "react-router";
import { getEntries } from "../api/entriesApi";
import type { Entry, getEntriesPayload, EntryFilters } from "../types/entry";
import EntriesFilters from "../components/entries/EntriesFilters";

interface LocationState {
    message?: string;
    type?: "success" | "error" | "info";
}

const empty_payload: getEntriesPayload = {
    start_date: null,
    end_date: null,
    tags: null,
}

const emptyFilters: EntryFilters = {
        start_date: "",
        end_date: "",
        tags: [],
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
    const [filters, setFilters] = useState<EntryFilters>(emptyFilters);

    async function handleAssistantSuccess() {
        const payload: getEntriesPayload = {
                    ...filters,
        };
        await load_entries(payload);
    }

    async function load_entries(payload: getEntriesPayload = empty_payload) {
        try {
            setIsLoading(true);
            setError("");

            const data = await getEntries(payload);
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

    useEffect(() => {
        const payload: getEntriesPayload = {
                ...filters,
        };
        void load_entries(payload);
    }, [filters]);

    return (
        <main>
           <section>
                <Link to="/entries/new">Add entry</Link>
           </section>
           <section>
                {message && (<p role={type === "error" ? "alert" : "status"}>{message}</p>)}
                {error && <p role="alert">{error}</p>}
           </section>
          <Assistant onSuccess={handleAssistantSuccess}/>
          <EntriesFilters onApply={load_entries} onFilter={setFilters} filters={filters}/>
           <section>
                <EntriesList entries={entries} isLoading={isLoading}/>
           </section>
        </main>
    )
}
