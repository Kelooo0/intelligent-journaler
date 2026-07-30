import type { EntryFilters, getEntriesPayload } from "../../types/entry"
import { useState } from "react"

type EntriesFiltersProps = {
    onApply: (payload?: getEntriesPayload) => Promise<void>;
    onFilter: React.Dispatch<React.SetStateAction<EntryFilters>>;
    filters: EntryFilters;
}

const emptyFilters: EntryFilters = {
        start_date: "",
        end_date: "",
        tags: [],
}

export default function EntriesFilters({
    onApply,
    onFilter,
    filters,
}: EntriesFiltersProps) {
    const MAX_TAGS = 5;
    const [tagInput, setTagInput] = useState("");

    function handleClear(): void {
        onFilter(emptyFilters);
        onApply();
    }
    function addTag(): void {
        const newTag = tagInput.trim();

        if(!newTag) {
            return;
        }
        if(filters.tags.length >= 5) {
            return;
        }
        if(filters.tags.includes(newTag)) {
            return;
        }
        onFilter((previousFilters) => ({
        ...previousFilters,
        tags: [...previousFilters.tags, newTag],
        }));
        setTagInput("");
    }
    function removeTag(tagToRemove: string):void {
        onFilter((previousFilters) => ({
        ...previousFilters,
        tags: previousFilters.tags.filter((tag) => tag !== tagToRemove,),
        }));
    }
    return (
        <section>
            <h1>Entries filters</h1>
            <form>
                <section>
                    <label htmlFor="start-date">Start date</label>
                    <input type="date" id="start-date" value={filters.start_date} onChange={(event) => onFilter({
                        ...filters,
                        start_date: event.target.value,
                    })}></input>
                </section>
                <br />
                <section>
                    <label htmlFor="end-date">End date</label>
                    <input type="date" id="end-date" value={filters.end_date} onChange={(event) => onFilter({
                        ...filters,
                        end_date: event.target.value
                    })}></input>
                </section>
                <br />
                <section id="tags">
                    <section className="tag-box">
                        <input type="text" name="tag" value={tagInput} placeholder="Enter tag name..." onChange={(event) => setTagInput(event.target.value)} disabled={filters.tags.length === MAX_TAGS}></input>
                        <button type="button" onClick={addTag} disabled={filters.tags.length === MAX_TAGS}>Add tag</button>
                    </section>
                    <section id="added-tags">
                        {filters.tags.map((tag) => (
                            <section key={tag} className="tag-item">
                                <span>{tag}</span>
                                <button type="button" onClick={() => removeTag(tag)}>Remove tag</button>
                            </section>
                        ))}
                    </section>
                </section>
                <section>
                    <button type="button" onClick={handleClear}>Clear filters</button>
                </section>
            </form>
        </section>
    )
}
