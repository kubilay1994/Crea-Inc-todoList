from sqlalchemy import Column, String, Integer
from sqlalchemy.sql.schema import ForeignKey

from app.db import Base


class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String(50), nullable=False)
    description = Column(String, nullable=False)
    video_link = Column(String)
    image_link = Column(String)

   
