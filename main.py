from fastapi import FastAPI
from routes import gifts, users

app = FastAPI(title="Gifters")

app.include_router(gifts.router)
app.include_router(users.router)