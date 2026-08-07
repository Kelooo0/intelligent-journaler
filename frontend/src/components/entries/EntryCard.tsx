import type { Entry } from "../../types/entry";
import { Link } from "react-router";
import "../../pages/EntryDetails.css";

type EntryCardProps = {
  entry: Entry;
  onDelete: (id: number) => void;
};

export default function EntryCard({ entry, onDelete }: EntryCardProps) {
  return (
    <article className="entry-details">
      <section className="entry-card-header-container">
        <section className="entry-card-id-container">
          <h3 className="entry-card-id">
            Entry -{" "}
            <time dateTime={entry.created_at}>
              {new Date(entry.created_at).toLocaleString("en-EN")}
            </time>
          </h3>
        </section>
        <section className="entry-card-ops">
          <Link
            className="entry-card-edit ec-op"
            to={`/entries/${entry.id}/edit`}
          >
            Edit
          </Link>
          <button
            className="entry-card-delete ec-op"
            type="button"
            onClick={() => onDelete(entry.id)}
          >
            Delete
          </button>
        </section>
      </section>
      <section className="entry-card-analysis">
        <section className="summary-container analysis-container">
          <p className="summary-header analysis-header">Summary:</p>
          <p className="summary-data analysis-data">{entry.summary}</p>
        </section>
        <section className="mood-container analysis-container">
          <p className="mood-header analysis-header">Mood:</p>
          <p className="mood-data analysis-data">{entry.mood}</p>
        </section>
        <section className="score-container analysis-container">
          <p className="score-header analysis-header">Sentiment score:</p>
          <p className="score-data analysis-data">{entry.sentiment_score}</p>
        </section>
        <section className="tags-container">
          <p className="tags-header analysis-header">Tags:</p>
          <section className="tags-data-container analysis-data">
            {entry.tags.length > 0 ? (
              entry.tags.map((tag) => (
                <span className="tag" key={tag.id}>
                  #{tag.name}
                </span>
              ))
            ) : (
              <span className="tag">none</span>
            )}
          </section>
        </section>
      </section>
      <section className="entry-card-content-container">
        <p className="entry-card-content">{entry.content}</p>
      </section>
    </article>
  );
}
