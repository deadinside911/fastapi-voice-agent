"""
Chat Services
"""
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from core.models import ChatHistory
from core.schemas.chat_schemas import ChatLogSchema
from . import DbSession, client

MAX_PREVIOUS_RECORDS = 5

SYSTEM_PROMPT = """
You are a historical chat companion.
Use prior conversation context when relevant.
Keep continuity naturally.
Do not invent memories outside conversation history.
""".strip()

class ChatServices:

    @staticmethod
    async def record_user_chat(payload: ChatLogSchema, session: AsyncSession) -> ChatHistory:
        """Persist an incoming user (or assistant) message to the DB."""
        entry = ChatHistory(
            conversation_id=payload.conversation_id,
            role=payload.role,
            content=payload.content,
        )

        session.add(entry)
        await session.commit()
        await session.refresh(entry)
        return entry

    @staticmethod
    async def get_conversation_window(conversation_id: str, session: AsyncSession) -> list[ChatHistory]:
        """
        Fetch the N most recent messages for this conversation
        and return them in chronological order (oldest → newest).
        This is the sliding context window.
        """
        statement = (
            select(ChatHistory)
            .where(ChatHistory.conversation_id == conversation_id)
            .order_by(ChatHistory.created_at.desc())   
            .limit(MAX_PREVIOUS_RECORDS)
        )

        result = await session.exec(statement)
        return list(reversed(result.all()))             

    @staticmethod
    async def generate_model_response(conversation_id: str, content: str, session: AsyncSession) -> str:
        """
        1. Save the incoming user message.
        2. Build the sliding context window from DB history.
        3. Call Gemini with system prompt + window + new message.
        4. Persist the assistant reply and return it.
        """
        # 1 — Persist the user turn
        user_payload = ChatLogSchema(
            conversation_id=conversation_id,
            role="user",
            content=content,
        )
        await ChatServices.record_user_chat(user_payload, session)

        # 2 — Sliding window: last N messages (already includes the one we just saved)
        window = await ChatServices.get_conversation_window(conversation_id, session)

        # 3 — Shape into the format Gemini's generate_content expects
        #     Each entry: {"role": "user"|"model", "parts": [{"text": "..."}]}
        #     Gemini uses "model" for assistant turns, not "assistant"
        history_contents = [
            {
                "role": "model" if msg.role == "assistant" else msg.role,
                "parts": [{"text": msg.content}],
            }
            for msg in window
        ]

        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.5-flash",
            contents=history_contents,
            config={
                "system_instruction": SYSTEM_PROMPT,
            },
        )

        assistant_text = response.text

        # 4 — Persist the assistant reply
        assistant_payload = ChatLogSchema(
            conversation_id=conversation_id,
            role="assistant",
            content=assistant_text,
        )
        await ChatServices.record_user_chat(assistant_payload, session)

        return assistant_text