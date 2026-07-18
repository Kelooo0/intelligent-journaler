from loguru import logger
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import UserModel
from app.schemas.schemas import Entry, EntryCreate, ToolData, ToolOutput, VectorResult
from app.services.entries_service import EntryService
from app.services.vector.base import VectorBase


class ToolExecutor:
    def __init__(self, vector: VectorBase, entry: EntryService):
        self.vector = vector
        self.entry = entry

    async def execute_tool(
        self,
        *,
        tool_calls: list[ToolData],
        current_user: UserModel,
        db: AsyncSession,
    ) -> list[ToolOutput]:
        used_tools = []
        for tool in tool_calls:
            tool_name = tool.name
            arguments = tool.arguments
            call_id = tool.call_id
            if tool_name == "get_entries":
                logger.debug(f"Calling {tool_name} for user_id: {current_user.id}")
                entries = await self.entry.get_entries_service(
                    db=db,
                    current_user=current_user,
                    start_date_str=arguments["start_date"],
                    end_date_str=arguments["end_date"],
                    tags=arguments["tags"],
                )
                serialized_entries = [Entry.model_validate(entry) for entry in entries]
                entries_json = (
                    TypeAdapter(list[Entry])
                    .dump_json(serialized_entries)
                    .decode("utf-8")
                )
                used_tools.append(
                    ToolOutput(name=tool_name, call_id=call_id, output=entries_json)
                )
            if tool_name == "create_entry":
                logger.debug(f"Calling {tool_name} for user_id: {current_user.id}")
                entry_content = EntryCreate(content=arguments["entry_data"]["content"])
                new_entry = await self.entry.create_entry_service(
                    entry_data=entry_content, db=db, current_user=current_user
                )
                serialized_entry = Entry.model_validate(new_entry)
                entry_json = serialized_entry.model_dump_json()
                used_tools.append(
                    ToolOutput(name=tool_name, call_id=call_id, output=entry_json)
                )
            if tool_name == "find_matching":
                logger.debug(f"Calling {tool_name} for user_id: {current_user.id}")
                matching_entries = await self.vector.find_matching(
                    query_content=arguments["query_content"],
                    start_date_str=arguments["start_date"],
                    end_date_str=arguments["end_date"],
                    current_user=current_user,
                    db=db,
                )
                matching_entries_json = (
                    TypeAdapter(list[VectorResult])
                    .dump_json(matching_entries)
                    .decode("utf-8")
                )
                used_tools.append(
                    ToolOutput(
                        name=tool_name, call_id=call_id, output=matching_entries_json
                    )
                )
        logger.info("Returning outputs of used tools")
        return used_tools
