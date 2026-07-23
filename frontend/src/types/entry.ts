export interface CreateEntryPayload {
    content: string;
}

export interface Tag {
    id: number;
    user_id: number;
    name: number;
}
export interface Entry {
    id: number;
    user_id: number;
    content: string;
    summary: string | null;
    mood: string | null;
    sentiment_score: number | null;
    created_at: string;
    tags: Tag[];
}
