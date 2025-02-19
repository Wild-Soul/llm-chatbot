from typing import List, Tuple, Optional
from threading import Lock
from ..repositories.chat_session import ChatSessionRepository
from ..repositories.message import MessageRepository
from ..schemas import MessageCreate, MessageEdit
from ..models import Message

class ChatService:
    _instance: Optional['ChatService'] = None
    _lock = Lock()
    
    def __init__(self):
        self.chat_session_repo: Optional[ChatSessionRepository] = None
        self.message_repo: Optional[MessageRepository] = None

    @classmethod
    def get_instance(cls) -> 'ChatService':
        # To create only singleton instance of a service.
        # Could be a better way to use __new__() rather than using locks.
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls()
        return cls._instance
    
    def initialize(self, chat_session_repo: ChatSessionRepository, message_repo: MessageRepository):
        """Initialize repositories - can be called with new db session"""
        self.chat_session_repo = chat_session_repo
        self.message_repo = message_repo
    
    async def get_or_create_session(self, session_id: str):
        session = self.chat_session_repo(session_id)
        if not session:
            session = self.chat_session_repo.create(id=session_id)
        else:
            session = self.chat_session_repo.activate_session(session_id)
        
        return session
    
    async def create_message(self, message: MessageCreate) -> Tuple[Message, Message]:
        if not self.chat_session_repo or not self.message_repo:
            raise RuntimeError("Service not initialized with repositories")
        
        # create user message
        user_message = self.message_repo.create(
            content=message.content,
            session_id=message.session_id,
            is_bot_message=False
        )

        # create bot response
        bot_message = self.message_repo.create(
            content="WIP, Stay Tuned!",
            session_id=message.session_id,
            is_bot_message=True,
            parent_message_id=user_message.id
        )

        return user_message, bot_message

    async def edit_message(self, message_id: int, message: MessageEdit, session_id: str) -> Tuple[Message, Message]:
        # Get and update the message
        updated_message = self.message_repo.update(
            message_id,
            content=message.content
        )

        if not updated_message or updated_message.session_id != session_id:
            raise ValueError("Message not found or unauthorized")

        if updated_message.is_deleted or updated_message.is_bot_message:
            raise ValueError("Cannot edit this message")
        
        # Handle bot response
        old_bot_response = self.message_repo.get_bot_resonse(message_id)
        if old_bot_response:
            self.message_repo.update(old_bot_response.id, is_deleted=True)
        
        new_bot_response = self.message_repo.create(
            content="WIP, stay tuned!",
            session_id=session_id,
            is_bot_message=True,
            parent_message_id=message_id
        )

        return updated_message, new_bot_response

    async def delete_message(self, message_id: int, session_id: str) -> Message:
        message = self.message_repo.get(message_id)

        if not message or message.session_id != session_id:
            raise ValueError("Message not found or unauthorized")

        if message.is_deleted or message.is_bot_message:
            raise ValueError("Cannot delete this message")
        
        return self.message_repo.update(message_id, is_deleted=True)
    
    async def get_session_messages(self, session_id: str) -> List[Message]:
        return self.message_repo.get_session_messages(session_id)
