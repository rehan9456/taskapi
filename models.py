from sqlalchemy import String , Integer , Boolean, ForeignKey
from sqlalchemy.orm import Mapped , mapped_column
from  sqlalchemy.orm import relationship 

from database import Base

class User(Base):
    __tablename__="users"

    id : Mapped[int] =mapped_column(Integer,primary_key=True,index=True)
    username:Mapped[str] = mapped_column(String(100),nullable=False)
    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )
    hashed_password:Mapped[str]=mapped_column(String(255),nullable=False)
    is_active:Mapped[bool]=mapped_column(Boolean,default=True)
    tasks=relationship("Task",back_populates="owner",cascade="all , delete-orphan")


class Task(Base):
    __tablename__ = "tasks"
    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
    title: Mapped[str]=mapped_column(String(150),nullable=False)
    description : Mapped[str| None]=mapped_column(String(150),nullable=True)
    completed : Mapped[bool] =mapped_column(Boolean,default=False,nullable=False)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False,index=True)
    owner = relationship("User",back_populates="tasks")
