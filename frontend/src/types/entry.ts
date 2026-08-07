export interface EntryPayload {
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

export interface EntryFilters {
  start_date: string;
  end_date: string;
  tags: string[];
}

export interface getEntriesPayload {
  start_date: string | null;
  end_date: string | null;
  tags: string[] | null;
}
