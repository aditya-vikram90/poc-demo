import os
from flask import Flask, jsonify
from pymongo import MongoClient
import redis
app = Flask(__name__)
r = redis.Redis.from_url(os.environ["REDIS_URL"])
db = MongoClient(os.environ["MONGO_URL"], serverSelectionTimeoutMS=3000).appdb
@app.get("/health")
def health():
    return "ok"
@app.get("/hit")
def hit():
    n = r.incr("hits")
    db.hits.insert_one({"n": n})
    return jsonify(site=os.environ.get("SITE", "?"), redis_hits=n, mongo_docs=db.hits.count_documents({}))
