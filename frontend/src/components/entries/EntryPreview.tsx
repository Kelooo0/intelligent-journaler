import type { Entry } from "../../types/entry"
import { Link } from "react-router";

type EntryPreviewProps = {
    entry: Entry;
};

export default function EntryPreview({
    entry,
}: EntryPreviewProps) {
    return (
    <article>
        <hr />
        <h2>Entry #{entry.id}</h2>
        <p>{entry.content}</p>
        <Link to={`/entries/${entry.id}/details`}>More...</Link>
        <hr />
    </article>
    )
}
