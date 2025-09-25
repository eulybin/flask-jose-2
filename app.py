import uuid
from flask import Flask, jsonify, request
from flask_smorest import abort
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
        abort(404, "Store not found.")


@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400, "Bad request. Ensure that the 'name' is included in the JSON body.")
    for store in stores:
        if store_data["name"] == store["name"]:
            abort(400, "This store already exists.")
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
        abort(404, "Item not found.")


@app.post("/item")
def create_item():
    item_data = request.get_json()

    # check that the json body includes the right props
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            "Bad request. Ensure that 'price', 'store_id', and 'name' are in the JSON payload.",
        )
    # loop through items and check if the item is already in our list
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, "Item already exists.")

    # make sure that the store which we want to add the item to exists
    if item_data["store_id"] not in stores:
        abort(404, "Store not found.")

    item_id = uuid.uuid4().hex
    new_item = {**item_data, "id": item_id}
    items[item_id] = new_item

    return new_item, 201
