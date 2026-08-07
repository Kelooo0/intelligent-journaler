import { useState } from "react";
import { updateEntry } from "../../api/entriesApi";
import { useNavigate } from "react-router";
import type { Entry } from "../../types/entry";
import "../../pages/EntryOp.css";

type EntryFormProps = {
  onError: (message: string) => void;
  entry: Entry;
};

export default function EntryUpdateForm({ onError, entry }: EntryFormProps) {
  const navigate = useNavigate();
  const [content, setContent] = useState(entry.content);
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: React.SubmitEvent<HTMLFormElement>) {
    event.preventDefault();
    try {
      setIsLoading(true);

      await updateEntry({ content }, entry.id);
      navigate(`/entries/${entry.id}/details`, {
        state: { message: "Entry updated succesfully.", type: "success" },
      });
    } catch (error) {
      onError(error instanceof Error ? error.message : "Failed to add entry.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="entry-form">
      <textarea
        id="content"
        className="entry-form-text"
        value={content}
        onChange={(event) => setContent(event.target.value)}
        disabled={isLoading}
      ></textarea>
      <button type="submit" className="entry-form-submit" disabled={isLoading}>
        {isLoading ? "Updating..." : "Update"}
      </button>
    </form>
  );
}
