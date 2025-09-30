from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from db import db


blueprint = Blueprint("Items", __name__, description="Operations on items")


# BLUEPRINT FOR SINGLE ITEM DATA
@blueprint.route("/item/<string:item_id>")
class Item(MethodView):
    @blueprint.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item was deleted."}

    @blueprint.arguments(ItemUpdateSchema)
    @blueprint.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()
        return item


# BLUEPRINT FOR ALL ITEMS DATA AND CREATE A NEW ITEM
@blueprint.route("/item")
class ItemList(MethodView):
    @blueprint.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blueprint.arguments(ItemSchema)
    @blueprint.response(201, ItemSchema)
    def post(self, item_data):
        new_item = ItemModel(**item_data)
        try:
            db.session.add(new_item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "An error occurred while inserting the item into the DB.")

        return new_item
