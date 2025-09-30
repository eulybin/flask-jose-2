import uuid
from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import StoreSchema
from models import StoreModel
from db import db


blueprint = Blueprint("Stores", __name__, description="Operations on stores")


# BLUEPRINT FOR SINGLE STORE DATA
@blueprint.route("/store/<string:store_id>")
class Store(MethodView):
    @blueprint.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store was deleted."}


# BLUEPRINT FOR ALL STORES AND CREATE A NEW STORE
@blueprint.route("/store")
class StoreList(MethodView):
    @blueprint.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blueprint.arguments(StoreSchema)
    @blueprint.response(201, StoreSchema)
    def post(self, store_data):
        new_store = StoreModel(**store_data)
        try:
            db.session.add(new_store)
            db.session.commit()

        except IntegrityError:
            abort(400, "A store with that name already exists.")

        except SQLAlchemyError:
            abort(500, "An error occurred while inserting the store into the DB.")
        return new_store
