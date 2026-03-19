from fastapi import FastAPI
from routes import gifts, users, auths, share
from database import init_db
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000"
]
app = FastAPI(title="Gifters")
app.add_middleware(
    CORSMiddleware, #It is a special layer that injects CORS headers into your responses, letting browsers know if a cross-origin request is allowed.
    allow_origins=origins, 
    allow_credentials=True,  #This allows cookies, authorization headers, or TLS client certificates to be sent along with the request.
    allow_methods=["*"], #Controls which HTTP methods are allowed in cross-origin requests.
    allow_headers=["*"] #Controls which custom headers can be sent in requests.
)
init_db()
app.include_router(gifts.router)
app.include_router(users.router)
app.include_router(share.router)
#app.include_router(auths.router)
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Gifters backend is running successfully 🎉"}