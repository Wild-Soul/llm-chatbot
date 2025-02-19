from .base import BaseRepository
from ..models import ChatSession
from datetime import datetime

class ChatSessionRepository(BaseRepository[ChatSession]):
    def activate_session(self, session_id: str) -> ChatSession:
        return self.update(
            session_id,
            last_active=datetime.now(),
            is_active=True
        )
    
    def deactivate_session(self, session_id: str) -> ChatSession:
        return self.update(
            session_id,
            is_active=False
        )
