from fastapi import FastAPI
from routes import gifts

app = FastAPI(title="Gifters")

app.include_router(gifts.router)