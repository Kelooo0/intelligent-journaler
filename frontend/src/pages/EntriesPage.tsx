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
import "./EntriesPage.css";

interface LocationState {
  message?: string;
  type?: "success" | "error" | "info";
}

const empty_payload: getEntriesPayload = {
  start_date: null,
  end_date: null,
  tags: null,
};

const emptyFilters: EntryFilters = {
  start_date: "",
  end_date: "",
  tags: [],
};

export default function EntriesPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const state = location.state as LocationState | null;
  const [error, setError] = useState("");
  const [message, setMessage] = useState(() => state?.message ?? "");
  const [type, setType] = useState(() => state?.type ?? "info");
  const [entries, setEntries] = useState<Entry[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filters, setFilters] = useState<EntryFilters>(emptyFilters);

  function clearMessage() {
    setError("");
    setMessage("");
    setType("info");
  }

  async function handleAssistantSuccess() {
    setError("");
    setMessage("");
    const payload: getEntriesPayload = {
      ...filters,
    };
    await load_entries(payload);
  }

  async function load_entries(payload: getEntriesPayload = empty_payload) {
    try {
      setIsLoading(true);

      const data = await getEntries(payload);
      setEntries(data);
    } catch (error) {
      setError(
        error instanceof Error ? error.message : "Failed to fetch entries.",
      );
      return;
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    if (state?.message) {
      navigate(location.pathname, {
        replace: true,
        state: null,
      });
    }
  }, [state?.message, navigate, location.pathname]);

  useEffect(() => {
    void load_entries();
  }, []);

  useEffect(() => {
    const payload: getEntriesPayload = {
      ...filters,
    };

    void load_entries(payload);
  }, [filters]);

  return (
    <main className="entries-main">
      <section className="entries-msgs">
        {message && (
          <p
            className="entries-message"
            role={type === "error" ? "alert" : "status"}
          >
            {message}
          </p>
        )}
        {error && (
          <p className="entries-message" role="alert">
            {error}
          </p>
        )}
      </section>
      <section className="entries-create-container">
        <Link to="/entries/new" className="entries-add-button">
          Add entry
        </Link>
      </section>
      <section className="entries-main-container">
        <EntriesFilters
          onAction={clearMessage}
          onClear={load_entries}
          onFilter={setFilters}
          filters={filters}
        />
        <EntriesList entries={entries} isLoading={isLoading} />
        <Assistant onSuccess={handleAssistantSuccess} onAction={clearMessage} />
      </section>
    </main>
  );
}
