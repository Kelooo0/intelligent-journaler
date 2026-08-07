import EntryCreateForm from "../components/entries/EntryCreateForm";
import { useState } from "react";
import "./EntryOp.css";

export default function EntryCreatePage() {
  const [error, setError] = useState("");

  return (
    <main className="entry-op-main">
      <section className="entry-op-header">
        <h1>Create a new entry</h1>
      </section>
      <section className="entry-form-container">
        <EntryCreateForm onError={setError} />
      </section>
      <section className="entry-op-msgs">
        {error && <p role="alert">{error}</p>}
      </section>
    </main>
  );
}
