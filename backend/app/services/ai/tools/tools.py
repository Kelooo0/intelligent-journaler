from openai.types.responses import FunctionToolParam

GET_ENTRIES_TOOL: FunctionToolParam = {
    "type": "function",
    "name": "get_entries",
    "description": (
        "Retrieves user's journal entries with optional filtering by date range and tags. "
        "If no filters are provided, returns all entries."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "start_date": {
                "type": "string",
                "format": "date",
                "description": (
                    "Inclusive start date in YYYY-MM-DD format. "
                    "If the user gives a day and month without a year, use the current year "
                    "from the system instructions. Never invent another year."
                ),
            },
            "end_date": {
                "type": "string",
                "format": "date",
                "description": (
                    "Inclusive end date in YYYY-MM-DD format. "
                    "For one specific day, use the same date as start_date. "
                    "If the year is omitted, use the current year."
                ),
            },
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Optional tags explicitly provided by the user for the journal entry. "
                    "Preserve the user's wording and language. "
                    "Do not generate, infer, translate, or add tags that the user did not provide."
                ),
            },
        },
        "required": [],
    },
}

CREATE_ENTRY_TOOL: FunctionToolParam = {
    "type": "function",
    "name": "create_entry",
    "description": ("Creates a new journal entry"),
    "parameters": {
        "type": "object",
        "properties": {
            "entry_data": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": (
                            "The exact journal entry content provided by the user. "
                            "Remove only command phrases used to request creation, such as "
                            "'create an entry', 'save this', or 'add to my journal'. "
                            "Preserve the user's original meaning, wording, language, tone, and details. "
                            "Do not summarize, rewrite, expand, correct, or add information."
                        ),
                    }
                },
            }
        },
        "required": ["entry_data"],
    },
}

FIND_MATCHING_TOOL: FunctionToolParam = {
    "type": "function",
    "name": "find_matching",
    "description": (
        "Finds the most relevant journal entries based on semantic similarity"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query_content": {
                "type": "string",
                "description": (
                    "A concise semantic search query derived from the user's request. "
                    "Remove command phrases such as 'show me' or 'find my entries' and remove "
                    "date expressions that are represented by start_date or end_date. "
                    "Preserve the user's original meaning, language, key topics, emotions, "
                    "events, people, and context. Do not add information that the user did not provide."
                ),
            },
            "start_date": {
                "type": "string",
                "format": "date",
                "description": (
                    "Inclusive start date in YYYY-MM-DD format. "
                    "If the user gives a day and month without a year, use the current year "
                    "from the system instructions. Never invent another year."
                ),
            },
            "end_date": {
                "type": "string",
                "format": "date",
                "description": (
                    "Inclusive end date in YYYY-MM-DD format. "
                    "For one specific day, use the same date as start_date. "
                    "If the year is omitted, use the current year."
                ),
            },
        },
    },
    "required": ["query_content", "dates"],
}
TOOLS: list[FunctionToolParam] = [
    GET_ENTRIES_TOOL,
    CREATE_ENTRY_TOOL,
    FIND_MATCHING_TOOL,
]
