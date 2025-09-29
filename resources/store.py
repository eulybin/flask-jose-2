import uuid
from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import stores
from schemas import StoreSchema


blueprint = Blueprint("Stores", __name__, description="Operations on stores")


# BLUEPRINT FOR SINGLE STORE DATA
@blueprint.route("/store/<string:store_id>")
class Store(MethodView):
    @blueprint.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, "Store not found.")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store was deleted."}
        except KeyError:
            abort(404, "Store not found.")


# BLUEPRINT FOR ALL STORES AND CREATE A NEW STORE
@blueprint.route("/store")
class StoreList(MethodView):
    @blueprint.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blueprint.arguments(StoreSchema)
    @blueprint.response(201, StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, "This store already exists.")
        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store
        return new_store
