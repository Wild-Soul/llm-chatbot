from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type
from app.models import Base

MT = TypeVar("MT", bound=Base)

class BaseRepository(Generic[MT]):
    def __init__(self, model: Type[MT], db: Session):
        self.model = model
        self.db = db
    
    def get(self, id: any) -> MT:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def create(self, **kwargs) -> MT:
        db_item = self.model(**kwargs)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def update(self, id: any, **kwargs) -> MT:
        db_item = self.get(id)
        if db_item:
            for key, value in kwargs.items():
                setattr(db_item, key, value)
            self.db.commit()
            self.db.refresh(db_item)
        return db_item
