from fastapi import WebSocket
from sqlalchemy.orm import Session
from typing import Dict
from app.schemas import MessageCreate, MessageEdit
from app.services import ChatService
from app.repositories import ChatSessionRepository, MessageRepository
from app.models import ChatSession, Message

class ChatController:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.chat_service = ChatService.get_instance()

    def initialize_service(self, db: Session) -> ChatService:
        """Initialize service with new db session"""
        chat_session_repo = ChatSessionRepository(ChatSession, db)
        message_repo = MessageRepository(Message, db)
        self.chat_service.initialize(chat_session_repo, message_repo)
        return self.chat_service

    async def connect(self, websocket: WebSocket, session_id: str, db: Session):
        service = self.initialize_service(db)
        await service.get_or_create_session(session_id)
        await websocket.accept()
        self.active_connections[session_id] = websocket

    async def disconnect(self, session_id: str, db: Session):
        service = self.initialize_service(db)
        await service.deactivate_session(session_id)
        if session_id in self.active_connections:
            del self.active_connections[session_id]

    async def handle_message(self, data: dict, session_id: str, db: Session):
        service = self.initialize_service(db)
        
        if data['type'] == 'message':
            messages = await service.create_message(
                MessageCreate(content=data['content'], session_id=session_id)
            )
            return {'type': 'message', 'messages': list(messages)}
        
        elif data['type'] == 'edit':
            messages = await service.edit_message(
                data['message_id'],
                MessageEdit(content=data['content']),
                session_id
            )
            return {'type': 'edit', 'messages': list(messages)}
        
        elif data['type'] == 'delete':
            message = await service.delete_message(data['message_id'], session_id)
            return {'type': 'delete', 'message': message}
