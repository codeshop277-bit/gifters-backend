from fastapi import FastAPI

app = FastAPI(title="Gifters API", version="0.1")

@app.get("/")
def root():
    return {"message": "Hello, Gifters!"}

@app.get("/ping")
def ping():
    return {"status": "ok"}

#app.get("/") → This decorator tells FastAPI:
#Whenever an HTTP GET request comes to /, call this function.”

#ef root(): → The function itself is the handler (like req, res in Express).

#eturn {"message": "Hello, Gifters!"} → Whatever you return becomes the HTTP response body (FastAPI automatically serializes dicts to JSON).

#Same idea: this function is the handler for GET /ping requests.

#hen you hit http://localhost:8000/ping, FastAPI calls ping(), gets back {"status": "ok"}, and sends it as JSON to the client.