from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from database import Base
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import relationship

class Gifts(Base):
    __tablename__ = "gifts"

    id = Column(Integer, primary_key=True, index=True) #primary_key creates unique id
    name = Column(String(150), nullable=False)
    brand = Column(String(150), nullable=True)
    size = Column(String(150), nullable=True)
    color = Column(String(150), nullable=True)
    link = Column(String(500), nullable=False)
    price = Column(Integer, nullable=False)
    note = Column(String(250), nullable=True)
    claimed = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable = False) #It ensures each gift must “belong to” a valid users.id.
    owner = relationship("User", back_populates="gifts",) #inks each gift back to its single owner (User).
    claimer=relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)
    password = Column(String(200), nullable=False)
    name = Column(String(100), nullable=False)

    gifts = relationship("Gifts", back_populates="owner") #“A single User can have many Gifts linked to them.”
    gifts_list=relationship("GiftsList", back_populates="user")

class RefreshTokens(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String(155), unique=True, nullable=False)

    user=relationship("User")

class ExternalUser(Base):
    __tablename__ = "external_users"

    id=Column(Integer, primary_key=True)
    google_id=Column(String(155), unique=True, index=True)
    name=Column(String(100))
    email=Column(String(100), unique=True)
    created_at=Column(DateTime, default=datetime.now(timezone.utc))

class GiftsList(Base):
    __tablename__ = "gifts_list"

    id=Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey("users.id"))
    created_at=Column(DateTime, default=datetime.now(timezone.utc))
    share_token=Column(String(155), unique=True, index=True, default=lambda: str(uuid.uuid4()))

    user=relationship("User", back_populates="gifts_list")

#relationship --> does not create a new column in db. It adds owner attribut in all gifts and gifts attributes in all users. 
    #So we can access gift.owner.name or users.gifts 
#back_populates connects two tables in relationship
#Foreign key --> Points to the primary key in another table, or Create a link between rows in two tables
    #i.e, Each gift belongs to one user from gift table
