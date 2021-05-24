from array import array
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pymongo
import json
import random
from typing import List
from typing import Optional

from fastapi import Query

from pymongo import cursor
client = pymongo.MongoClient(
    "connectionString")
db = client["victorinaZhivotnie"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/nameById")
async def getnameById(id: int):
    res = []
    cursor = db.question
    for i in cursor.find({'id': id}):
        res.append({"name": i['name']})
    return res


def Convert(string):
    li = list(string.split(","))
    res = []
    for i in li:
        res.append(int(i))
    return res


@app.get("/randomAnimal")
async def getRandomAnimal(solvedQuestions: str):
    listnumbers = []
    if solvedQuestions != "":
        listnumbers = Convert(solvedQuestions)
    print(listnumbers)

    count = db.question.count() - 1

    r = list(range(0, count))

    for i in listnumbers:
        r.remove(i)

    # random_index = int(random.randint(0, count))
    # print("COUNT", count)
    result = {}
    # print("random_index", random_index)

    response = db.question.find_one({"id": random.choice(r)})
    result["id"] = response["id"]
    result["name"] = response["name"]
    result["picture"] = response["picture"]
    result["sound"] = response["sound"]
    result["description"] = response["description"]
    return result


@app.get("/pictureById")
async def getpictureById(id: int):
    res = []
    cursor = db.question
    for i in cursor.find({'id': id}):
        res.append({"picture": i['picture'][:10]})
    return res


@app.get("/soundById")
async def getsoundById(id: int):
    res = []
    cursor = db.question
    for i in cursor.find({'id': id}):
        res.append({"sound": i['sound'][:10]})
    return res


@app.get("/descriptionById")
async def descriptionById(id: int):
    res = []
    cursor = db.question
    for i in cursor.find({'id': id}):
        res.append({"sound": i['sound'][:10]})
    return res


@app.get("/allQuestions")
async def allQuestions():
    res = []
    cursor = db.question
    for i in cursor.find({}, {'_id': 0}):
        res.append(i)
    return res
