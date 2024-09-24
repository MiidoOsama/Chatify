# app.py
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from database.models import ServerModel
from database.schemas import ServerSchema
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Connect with mongodb
client = MongoClient("mongodb+srv://chatify:chatify@chatify.dzioy.mongodb.net/?retryWrites=true&w=majority&appName=Chatify")
db = client["chatify"]
servers_collection = db["servers"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
# 1. Get all servers
@app.get("/servers")
def get_all_servers():
    servers = list(servers_collection.find())
    for server in servers:
        server["_id"] = str(server["_id"])
    return servers

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
    return {"id": str(result.inserted_id)}

# 4. Update a server by ID
@app.put("/servers/update/{id}")
def update_server(id: str, server: ServerSchema):
    updated_server = servers_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": server.dict()},
        return_document=True
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
