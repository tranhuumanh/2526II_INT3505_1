from flask import request
from bson import ObjectId

def get_all():
    from app import mongo
    # Lấy dữ liệu từ collection 'products'
    products = list(mongo.db.products.find())
    for p in products:
        p['_id'] = str(p['_id'])
    return products, 200

def create():
    from app import mongo
    body = request.get_json()
    result = mongo.db.products.insert_one({
        "name": body.get("name"),
        "price": body.get("price"),
        "description": body.get("description", "")
    })
    return {"id": str(result.inserted_id), "message": "Success"}, 201