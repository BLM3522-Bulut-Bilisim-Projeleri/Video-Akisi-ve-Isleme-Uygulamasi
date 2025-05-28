from pymongo import MongoClient
import datetime

def connect_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["video_analysis"]
    collection = db["labels"]
    return collection

def save_labels_to_db(video_name, labels):
    collection = connect_mongo()
    now = datetime.datetime.utcnow()

    for label in labels:
        document = {
            "video": video_name,
            "label": label["label"],
            "start_time": label["start_time"],
            "end_time": label["end_time"],
            "confidence": label["confidence"],
            "bounding_box": label.get("bounding_box", None),  
            "analyzed_at": now
        }
        collection.insert_one(document)

    print(f"{len(labels)} etiket MongoDB'ye kaydedildi.")

def get_labels_from_db(video_name):
    collection = connect_mongo()
    labels = list(collection.find({"video": video_name}))
    return labels