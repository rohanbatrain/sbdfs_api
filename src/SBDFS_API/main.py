from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

db_client = MongoClient("mongodb://localhost:27017/")
db = db_client["sbd"]
collection = db["files"]

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_file():
    data = request.json
    
    if not data or "path" not in data or "stat" not in data or "content" not in data:
        return jsonify({"error": "Invalid data format"}), 400
    
    # Ensure path is unique
    if collection.find_one({"path": data["path"]}):
        return jsonify({"error": "File with this path already exists"}), 400
    
    # Store data in MongoDB
    file_doc = {
        "path": data["path"],
        "stat": data["stat"],
        "content": data["content"],
        "type": data["type"]
    }
    result = collection.insert_one(file_doc)
    
    return jsonify({"message": "File data stored", "id": str(result.inserted_id)}), 201

@app.route("/download/<path:file_path>", methods=["GET"])
def download_file(file_path):
    file_doc = collection.find_one({"path": file_path})
    
    if not file_doc:
        return jsonify({"error": "File not found"}), 404
    
    return jsonify({
        "path": file_doc["path"],
        "stat": file_doc["stat"],
        "content": file_doc["content"],
        "type": file_doc["type"]
    }), 200




if __name__ == "__main__":
    app.run(debug=True)
