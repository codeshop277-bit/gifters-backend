from fastapi import FastAPI
from routes import gifts, users, auths
from database import init_db

app = FastAPI(title="Gifters")
init_db()
app.include_router(gifts.router)
app.include_router(users.router)
#app.include_router(auths.router)