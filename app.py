import uuid
from flask import Flask, jsonify, request
from data import stores, items


app = Flask(__name__)


# routes for STORES
@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}, 200


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message": "Store not found."}, 404


@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201


# routes for ITEMS
@app.get("/item")
def get_items():
    return {"items": list(items.values())}, 200


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message": "Item not found."}, 404


@app.post("/item")
def create_item():
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"message": "Store not found."}, 404

    item_id = uuid.uuid4().hex
    new_item = {**item_data, "id": item_id}
    items[item_id] = new_item

    return new_item, 201
