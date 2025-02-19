from sqlalchemy import Column, Integer, ForeignKey, String, Date, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String, ForeignKey("chat_session.id"), index=True, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
    is_bot_message = Column(Boolean, default=False)
    parent_message_id = Column(Integer, ForeignKey("messages.id"), nullable=True) # to simulate "replied to" scenario

    session = relationship("ChatSession")
    replies = relationship("Message", backref="parent_message")
