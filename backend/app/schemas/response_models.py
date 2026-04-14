from datetime import date
from typing import Dict, List, Literal

from pydantic import BaseModel


class LongestMessageItem(BaseModel):
    Author: str
    Message: str
    Length: int


class StreakItem(BaseModel):
    start: date
    end: date
    duration: int


class ChatStatsPayload(BaseModel):
    status: Literal["success", "failed"]
    message: str
    total_messages: int
    participants: List[str]
    total_users: int
    n_messages_per_user: Dict[str, int]
    hot_hours: Dict[str, int]
    messages_per_day: Dict[str, int]
    messages_per_month: Dict[str, int]
    messages_per_year: Dict[str, int]
    top_messages_per_day: Dict[str, int]
    top_words: Dict[str, int]
    top_emojis: Dict[str, int]
    longest_messages: List[LongestMessageItem]
    top_streaks: List[StreakItem]


class AnalyzeChatDataResponse(BaseModel):
    status: Literal["success"]
    stats: ChatStatsPayload
