from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#create_engine → Creates a connection to the database (engine is the “core” interface to the DB)
#sessionmaker ->Factory for creating new Session objects (sessions are used to talk to the DB).

DATABASE_URL = "mysql+mysqlconnector://root:balaji27@localhost:3307/giftersdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()   # creates a new session

Base = declarative_base() #A factory function that creates a base class. All ORM models inherit from this base so SQLAlchemy knows how to map classes to tables.

def init_db():
    Base.metadata.create_all(bind=engine)  #looks at all classes that inherit from Base (e.g., your Gift model).

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#So when you call init_db(), SQLAlchemy will create all tables defined in your models inside your gifters database.
# class GiftCreate(BaseModel):
#     name: str
#     brand: Optional[str] = None
#     size: Optional[str] = None
#     color: Optional[str] = None

# class Gift(GiftCreate):
#     id: str


# gifts_db: list[Gift] = [Gift(id= '1', name='test', size='M', color="Red")]

gifts_mock = [
        {"id": 1, "name": "Shirt", "brand": "Nike", "price": 40},
        {"id": 2, "name": "Cap", "brand": "Adidas", "price": 25},
        {"id": 3, "name": "Shoes", "brand": "Nike", "price": 90},
    ]

users_list = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com"
    },
    {
        "id": 2,
        "name": "Bob Smith",
        "email": "bob.smith@example.com"
    },
    {
        "id": 3,
        "name": "Charlie Brown",
        "email": "charlie.brown@example.com"
    }
]