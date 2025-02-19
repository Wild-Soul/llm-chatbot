from .base import BaseRepository
from ..models import Message
from sqlalchemy import desc

class MessageRepository(BaseRepository[Message]):
    def get_session_messages(self, session_id: str):
        return self.db.query(self.model).filter(
            self.model.session_id == session_id,
            self.model.is_deleted == False
        ).order_by(self.model.created_at.asc).all()

    def get_bot_resonse(self, message_id: int):
        return self.db.query(self.model).filter(
            self.model.parent_message_id == message_id,
            self.model.is_bot_message == True
        ).first()
