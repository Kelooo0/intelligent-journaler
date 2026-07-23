import type { Entry } from "../../types/entry";

type EntryResultProps = {
    result: Entry;
};

export default function CreateEntryResult({
    result,
}: EntryResultProps) {
    return (
        <section>
            <h2>{result.content}</h2>
            <p>{result.summary}</p>
            <p>{result.mood}</p>
            <p>{result.sentiment_score}</p>
            {result.tags.map((tag) => (<p key={tag.id}>{tag.name}</p>))}
        </section>
    )
}
