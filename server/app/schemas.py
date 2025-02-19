from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatSessionCreate(BaseModel):
    session_id: str

class ChatSessionResponse(BaseModel):
    id: str
    created_at: datetime
    last_active: datetime
    last_active: bool

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    session_id: str

class MessageEdit(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    session_id: str
    created_at: datetime
    updated_at: Optional[datetime]
    is_deleted: bool
    is_bot_message: bool
    parent_message_id: Optional[int]

    class Config:
        from_attributes = True