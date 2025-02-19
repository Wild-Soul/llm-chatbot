from sqlalchemy import Column, Integer, ForeignKey, String, Date, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String, ForeignKey("chat_sessions.id"), index=True, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
    is_bot_message = Column(Boolean, default=False)
    parent_message_id = Column(Integer, ForeignKey("messages.id"), nullable=True) # to simulate "replied to" scenario

    session = relationship("ChatSession")
    replies = relationship("Message", backref="parent_message", remote_side=[id])


    def as_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_deleted": self.is_deleted,
            "is_bot_message": self.is_bot_message,
            "parent_message_id": self.parent_message_id,
        }
