from flask import Flask, jsonify, request
from stores import stores


app = Flask(__name__)


@app.get("/store")
def get_stores():
    return jsonify(stores), 200


@app.post("/store/<string:store_name>")
def add_store(store_name):
    data = request.get_json()
    for store in stores:
        if store["store_name"] == store_name:
            new_item = {"item_name": data["item_name"], "price": data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "No such store found."}, 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
