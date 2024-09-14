from fastapi import FastAPI
import uvicorn
from utils import (
    getcategoriesFromImage,
    getCategoriesFromText,
    getCategoriesFromQuery,
    getImage,
)
from similarity import find_top_k_similar
import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import sys

load_dotenv()

database_path = os.getenv("SAMPLE_DATABASE_NORMAL")
images_path = os.getenv("SAMPLE_DATABASE_IMAGE")

mongoDatabase = MongoClient(os.getenv("CONNECTION_STRING"))["bhAIya"]

# DATABASE_NAME="database"
# DATABASE_NAME="database_500"
# DATABASE_NAME="amazon_database"
DATABASE_NAME = "only_clothes"

# IMAGES_DATABASE= "imageDatabase"
# IMAGES_DATABASE= "imageDatabase_500"
# IMAGES_DATABASE = "amazon_images"
IMAGES_DATABASE = "only_clothes_images"
# IMAGES_DATABASE = "merged_images_3.6" 



try:
    # database = mongoDatabase["database"].find({}, {"_id": 0})
    # database = mongoDatabase["database_500"].find({}, {"_id": 0})
    database = mongoDatabase[DATABASE_NAME].find({}, {"_id": 0})
    database = list(database)
    print("Data loaded")
except Exception as e:
    print("Error loading main database")
try:
    # imgDatabase = mongoDatabase["imageDatabase"].find({}, {"_id": 0})
    # imgDatabase = mongoDatabase["imageDatabase_500"].find({}, {"_id": 0})
    imgDatabase = mongoDatabase[IMAGES_DATABASE].find({}, {"_id": 0})
    imgDatabase = list(imgDatabase)
    print("Image database loaded")
except Exception as e:
    print("Erorr loading image database")

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "App is running"}


@app.post("/data")
async def data(data: dict):
    # database=None
    # imgDatabase=None
    textCategories = None
    imgCategories = None
    # try:
    #     with open(database_path,"r") as f:
    #         database=json.load(f)
    # except Exception as e:
    #     print(f"An error occured while reading the database: {e}")
    # try:
    #     with open(images_path,"r") as f:
    #         imgDatabase=json.load(f)
    # except Exception as e:
    #     print(f"An error occured while reading the image database: {e}")
    text = data.get("text", None)
    img64 = data.get("img64", None)
    if img64:
        if img64[0] == "b":
            img64 = img64[2:-1]
    categories = {}
    print(text)
    if text != None:
        textCategories = getCategoriesFromQuery("mistral:latest", text, ollama=True)[
            "categories"
        ][0]
    if img64 != None:
        imgCategories = getcategoriesFromImage(
            "llava-phi3:latest", imagePath=None, imgb64=img64, ollama=True
        )["categories"][0]
    if text != None and img64 != None:
        for key in textCategories.keys():
            categories[key] = list(set(textCategories[key] + imgCategories[key]))
    elif text != None:
        categories = textCategories
    else:
        categories = imgCategories
    print(categories)
    results = find_top_k_similar(categories, database, top_k=5)
    l = []
    for result in results:
        result[1]["image"] = getImage(imgDatabase, result[1]["id"])
        l.append(result[1])
    return l


@app.post("/addOne")
async def addOne(data: dict):
    """
    Payload
    {"data":{
                "id":0,
                "price":123,
                "Main category":[],
                "Sub categories":[],
                "Additional details":[]
            },
            "imgData":{
                  "id":0,
                  "image":"b'/9j/4AAQSk'"
              }
    }
    """
    if data.get("data", None):
        print("inserting into main database")
        try:
            x = mongoDatabase["database"].insert_one(data["data"])
            print(x)
        except Exception as e:
            print(e)
            print("Error inserting into main database")

    if data.get("imgData", None):
        print("inserting into image database")
        try:
            x = mongoDatabase["imageDatabase"].insert_one(data["imgData"])
            print(x)
        except Exception as e:
            print("Error inserting into image database")


@app.post("/removeOne")
async def removeOne(data: dict):
    """
    Payload : 0(any integer, id to be removed)
    """
    id = data["id"]
    print("deleting from database")
    try:
        x = mongoDatabase["database"].delete_one({"id": id})
        print(x)
    except Exception as e:
        print("Error deleting from main database")

    try:
        x = mongoDatabase["imageDatabase"].delete_one({"id": id})
        print(x)
    except Exception as e:
        print("Error deleting image database")


@app.post("/addMany")
async def addMany(data: dict):
    """
    payload
    {
        "data":[{
            "id":0,
            "price":123,
            "Main category":[],
            "Sub categories":[],
            "Additional details":[]
        },{
            "id":0,
            "price":123,
            "Main category":[],
            "Sub categories":[],
            "Additional details":[]
        }],
        "imgData":[{
            "id":0,
            "image":"b'/9j/4AAQSk'"

        },{
            "id":0,
            "image":"b'/9j/4AAQSk'"

        }]
    }
    """
    if data.get("data", None):
        print("inserting many into database")
        try:
            x = mongoDatabase["database"].insert_many(data.get("data"))
            print(x)
        except Exception as e:
            print("Error inserting many into main database")

    if data.get("imgData", None):
        try:
            x = mongoDatabase["imageDatabase"].insert_many(data.get("imgData"))
            print(x)
        except Exception as e:
            print("Error inserting many into image database")


@app.post("/getCategories")
async def getCategories(data: dict):
    id = data["id"]
    # data=mongoDatabase["database"].find({"id":int(id)},{"_id":0})
    # data=mongoDatabase["database_500"].find({"id":str(id)},{"_id":0})
    try:
        data = mongoDatabase[DATABASE_NAME].find({"id": str(id)}, {"_id": 0})
        imageData = getImage(imgDatabase, str(id))
        data_send = list(data)[0]

    except Exception as e:
        data = mongoDatabase[DATABASE_NAME].find({"id": int(id)}, {"_id": 0})
        imageData = getImage(imgDatabase, int(id))
        data_send = list(data)[0]
    data_send["image"] = imageData
    print(data_send)
    return data_send


@app.get("/getHistory")
async def getHistory(data: dict):
    id = data["currentConversationId"]
    data = mongoDatabase["history"].find({"currentConversationId": id}, {"_id": 0})
    data = list(data)[0]
    return data


@app.post("/addHistory")
async def addHistory(data: dict):
    incoming_data = data
    id = incoming_data["currentConversationId"]
    current_data = mongoDatabase["history"].find(
        {"currentConversationId": id}, {"_id": 0}
    )
    current_data = list(current_data)
    if current_data != []:
        conversations = incoming_data["conversations"]
        last_updated = incoming_data["last_updated"]
        x = mongoDatabase["history"].update_one(
            {"currentConversationId": id},
            {"$set": {"conversations": conversations, "last_updated": last_updated}},
        )
        print(x)
    else:
        x = mongoDatabase["history"].insert_one(data)
        print(x)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5004)
