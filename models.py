from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Gifts(Base):
    __tablename__ = "gifts"

    id = Column(Integer, primary_key=True, index=True) #primary_key creates unique id
    name = Column(String(150), nullable=False)
    brand = Column(String(150), nullable=True)
    size = Column(String(150), nullable=True)
    color = Column(String(150), nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable = False) #It ensures each gift must “belong to” a valid users.id.
    owner = relationship("User", back_populates="gifts") #inks each gift back to its single owner (User).

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    name = Column(String(100), nullable=False)

    gifts = relationship("Gifts", back_populates="owner") #“A single User can have many Gifts linked to them.”