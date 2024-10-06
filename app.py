# app.py
from fastapi import FastAPI, HTTPException, Query, Depends, Request,status
from pymongo import MongoClient
from database.models import ServerModel
from database.schemas import ServerSchema , User
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from oauth import get_current_user
from jwttoken import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from hashing import Hash


app = FastAPI()

# Connect with mongodb
client = MongoClient(
    "mongodb+srv://chatify:chatify@chatify.dzioy.mongodb.net/?retryWrites=true&w=majority&appName=Chatify"
)
db = client["chatify"]
servers_collection = db["servers"]
# Collection for users
users_collection = db["users"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register")
def create_user(request: User):
    hashed_pass = Hash.bcrypt(request.password)
    user_object = dict(request)
    user_object["password"] = hashed_pass
    user_id = db["users"].insert_one(user_object).inserted_id
    return {"res": "created"}


@app.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends()):
    user = db["users"].find_one({"username": request.username})
    if not user:
        raiseHTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not Hash.verify(user["password"], request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


# 1. Get all servers
@app.get("/servers", response_model=List[dict])
def get_all_servers(
    page: int = Query(1, ge=1), page_size: int = Query(8, ge=1, le=100)
):
    # Calculate the number of items to skip
    skip = (page - 1) * page_size

    # Retrieve data from MongoDB using skip and limit
    servers = list(servers_collection.find().skip(skip).limit(page_size))

    # Convert _id to string
    for server in servers:
        server["_id"] = str(server["_id"])

    # Calculate the total number of servers
    total_servers = servers_collection.count_documents({})
    total_pages = (total_servers + page_size - 1) // page_size  # Calculate total pages

    # Return the result
    return {
        "page": page,
        "page_size": page_size,
        "total_servers": total_servers,
        "total_pages": total_pages,
        "data": servers,
    }


# 2. Get server by ID
@app.get("/servers/{id}")
def get_server_by_id(id: str):
    server = servers_collection.find_one({"_id": ObjectId(id)})
    if server:
        server["_id"] = str(server["_id"])
        return server
    raise HTTPException(status_code=404, detail="Server not found")


# 3. Create a new server
@app.post("/servers/create")
def create_server(server: ServerSchema):
    new_server = ServerModel(**server.dict())
    result = servers_collection.insert_one(new_server.to_dict())
    try:
        return {
            "id": str(result.inserted_id),
            "message": "Created Sucessfully",
            "status": True,
        }
    except Exception as e:
        return {"message": "There is something wrong!", "status": False}


# 4. Update a server by ID
@app.put("/servers/update/{id}")
def update_server(id: str, server: ServerSchema):
    updated_server = servers_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": server.dict()}, return_document=True
    )
    if updated_server:
        updated_server["_id"] = str(updated_server["_id"])
        return updated_server
    raise HTTPException(status_code=404, detail="Server not found")


# 5. Delete a server by ID
@app.delete("/servers/delete/{id}")
def delete_server(id: str):
    result = servers_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"detail": "Server deleted"}
    raise HTTPException(status_code=404, detail="Server not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
