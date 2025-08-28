from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
#pydantic is a Python library that validates and structures data.
#BaseModel is its main class — you use it to define the shape of data (like a schema)
from typing import Optional
#Optional[T] means: the value can either be type T or None.
#(None in Python ≈ null in JS)
#If you want a field in your API request to be not mandatory, you mark it Optional.
import uuid

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

@app.get("/gifts")
def get_gifts_list():
    #mock data
    gifts =  [
        {"id": 1, "name": "Shirt", "brand": "Nike"},
        {"id": 2, "name": "Watch", "brand": "Fossil"}
    ]
    return {"results": gifts}

@app.get("/user/{user_id}")
def getUser(user_id: int):
    return {"id": user_id, "name": "Test"}

@app.get("/users/db/{user_id}")
def get_users_from_db(user_id: int):
    #Mock data
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
    results = next((user for user in users_list if user["id"] == user_id), None)

    if results is None:
        raise HTTPException(status_code=404, detail= f"User with id {user_id} does not exist")

    return {"results": results}
# next(iterator, default)
#next(...) is a Python built-in that returns the first item from an iterator.
#f the iterator has an item → return it.
#f it’s empty → raise StopIteration unless you provide a default.

class GiftCreate(BaseModel):
    name: str
    brand: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None

class Gift(GiftCreate):
    id: str     

gifts_db : list[Gift] = [Gift(id="1", name="test")]

@app.get("/gifts-list")
def gifts_list():
    return gifts_db

@app.post("/add-gift", response_model=Gift) # response_model=Gift this prevets from sending the whole payload as repsonse. Only params which matches the Gift will be returned
def add_gifts(gift: GiftCreate):
    new_gift = Gift(id = str(uuid.uuid4()), **gift.model_dump())
    gifts_db.append(new_gift)
    return {"gift added to db": new_gift}
#uuid - universally unique identifier library
# model_dump - turns python modal into plain dictionary
# **gift **gift.model_dump()  applies model_dump to the entire gift attribute

#** is the dictionary unpacking operator.

@app.get("/gifts/{gift_id}", response_model= Gift)
def get_gift(gift_id: str): 
    for gift in gifts_db:
        if gift.id == gift_id:
            return gift
        return {"error": "Gift not found"}

@app.delete("/gifts/remove/{gift_id}", response_model=dict)
def remove_gift(gift_id: str):
    for gift in gifts_db:
        if gift.id == gift_id:
            gifts_db.remove(gift)
            return {"message": "Gift removed successfully"}
    raise HTTPException(status_code=404, detail="Gift Not found")

@app.put("/gifts/update/{gift_id}", response_model=Gift)
def update_gift(gift_id: str, updated_gift: GiftCreate):
    for index, gift in enumerate(gifts_db): #enumerate lets you loop with both: index and item
        if gift.id == gift_id:
            new_gift = Gift(id=gift_id, **updated_gift.model_dump())
            gifts_db[index] = new_gift
            return new_gift
    raise HTTPException(status_code=404, detail="Gift not found")

class GiftPatch(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
@app.patch("/gifts/patch/{gift_id}", response_model=Gift)
def patch_gift(gift_id: str, patch_gift: GiftPatch):
    for index, gift in enumerate(gifts_db):
        if gift.id == gift_id:
            new_data = patch_gift.model_dump(exclude_unset=True) #exclude_unset=True removes fields the user didn’t send.
            updated_gift = gift.model_copy(update= new_data)
            gifts_db[index]   = updated_gift
            return updated_gift
    raise HTTPException(status_code=404, detail="Gift not found")