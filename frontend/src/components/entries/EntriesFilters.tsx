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
    const [error, setError] = useState("");

    function handleClear(): void {
        setError("");
        onFilter(emptyFilters);
        onApply();
    }
    function addTag(): void {
        setError("");
        const newTag = tagInput.trim();

        if(!newTag) {
            setError("Tag name can't be empty.");
            return;
        }
        if(newTag.length < 3 || newTag.length > 20) {
            setError("Tag name must contain between 3 and 20 characters.");
            return;
        }
        if(filters.tags.length >= 5) {
            setError("You can only add up to 5 tags.");
            return;
        }
        if(filters.tags.includes(newTag)) {
            setError(`${newTag} is already added to tags.`);
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
        <section className="filters-container">
            <section className="filters-header-container">
                <h2 className="filters-header">Entries filters</h2>
            </section>
            <section className="filters-button-container">
                <button className="clear-filters" type="button" onClick={handleClear}>Clear filters</button>
            </section>
            <section className="filters-form-container">
                <form className="filters-form">
                    <section className="sd-container">
                        <label className="sd-label" htmlFor="start-date">Start date</label>
                        <input className="sd-value" type="date" id="start-date" value={filters.start_date} onChange={(event) => onFilter({
                            ...filters,
                            start_date: event.target.value,
                        })}></input>
                    </section>
                    <section className="ed-container">
                        <label className="ed-label" htmlFor="end-date">End date</label>
                        <input className="ed-value" type="date" id="end-date" value={filters.end_date} onChange={(event) => onFilter({
                            ...filters,
                            end_date: event.target.value
                        })}></input>
                    </section>
                    <section className="filters-tags-container">
                        <section className="add-tag-container">
                            <input className="add-tag-text" type="text" name="tag" value={tagInput} placeholder="Enter tag name..." onChange={(event) => setTagInput(event.target.value)} disabled={filters.tags.length === MAX_TAGS}></input>
                            <button className="add-tag-submit" type="button" onClick={addTag} disabled={filters.tags.length === MAX_TAGS}>Add</button>
                        </section>
                        <section className="added-tags">
                            <p className="added-tags-header">Added tags:</p>
                            {filters.tags.map((tag) => (
                                    <section className="added-tag-container">
                                        <p className="added-tags-item" onClick={() => removeTag(tag)}>#{tag}</p>
                                    </section>
                            ))}
                        </section>
                    </section>
                </form>
            </section>
            <section className="filters-messages">
                {error && <p role="alert">{error}</p>}
            </section>
        </section>
    )
}
