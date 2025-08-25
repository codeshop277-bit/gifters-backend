from fastapi import FastAPI
from pydantic import BaseModel
#pydantic is a Python library that validates and structures data.
#BaseModel is its main class — you use it to define the shape of data (like a schema)
from typing import Optional
#Optional[T] means: the value can either be type T or None.
#(None in Python ≈ null in JS)
#If you want a field in your API request to be not mandatory, you mark it Optional.

app = FastAPI(title="Gifters API", version="0.1")

class EchoPayload(BaseModel):
    text: str
    repeat: int = 1
# EchoPayload is similar to body balidation all the payload props shoul present here simsilar to typescript custom types
@app.get("/")
def root():
    return {"message": "Hello, Gifters!"}

@app.get("/ping")
def ping():
    return {"status": "ok"}

#app.get("/") → This decorator tells FastAPI:
#Whenever an HTTP GET request comes to /, call this function.”

@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"hello, {name}"}

@app.get("/greet-adv/{name}")
def greet_adv(name: str, excited: bool = False, times: int = 1):
    message = ("Hello," + name + " " + ("!" if excited else ".")) * max(times, 1)
    return {"message": message}
#f - formatted string iteral, required to inject dynamic values to text. Similar to `${name}` in react

@app.post("/echo")
def echo(payload: EchoPayload):
    return {"echo": payload.text * max(payload.repeat, 1)}

#ef root(): → The function itself is the handler (like req, res in Express).

#eturn {"message": "Hello, Gifters!"} → Whatever you return becomes the HTTP response body (FastAPI automatically serializes dicts to JSON).

#Same idea: this function is the handler for GET /ping requests.

#hen you hit http://localhost:8000/ping, FastAPI calls ping(), gets back {"status": "ok"}, and sends it as JSON to the client.

@app.get("/gifts/search")
def gifts_search(brand: Optional[str] = None, max_price: Optional[int] = None):
    #mock data 
    gifts = [
        {"id": 1, "name": "Shirt", "brand": "Nike", "price": 40},
        {"id": 2, "name": "Cap", "brand": "Adidas", "price": 25},
        {"id": 3, "name": "Shoes", "brand": "Nike", "price": 90},
    ]
    results = [
        gift for gift in gifts
        if(brand is None or gift["brand"].lower() == brand.lower()) and (max_price is None or gift['price'] <= max_price)
    ]
    return {"results": results}