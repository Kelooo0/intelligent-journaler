import type { Entry } from "../../types/entry"
import { Link } from "react-router";

type EntryCardProps = {
    entry: Entry;
    onDelete: (id: number) => void;
};

export default function EntryCard({
    entry,
    onDelete
}: EntryCardProps) {
    return (
    <article>
        <hr />
        <h3>Entry: #{entry.id}</h3>
        <p>Content: {entry.content}</p>
        <p>Summary: {entry.summary}</p>
        <p>Mood: {entry.mood}</p>
        <p>Sentiment score: {entry.sentiment_score}</p>
        <p>Tags:</p>
        <ul>
            {entry.tags.map((tag) => (<li key={tag.id}>{tag.name}</li>))}
        </ul>
        <time dateTime={entry.created_at}>
            {new Date(entry.created_at).toLocaleString("en-EN")}
        </time>
        <Link to={`/entries/${entry.id}`}>More...</Link>
        <Link to={`/entries/${entry.id}/edit`}>Edit</Link>
        <button type="button" onClick={() => onDelete(entry.id)}>Delete</button>
        <hr />
    </article>
    )
}
