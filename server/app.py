from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route("/messages", methods=["GET", "POST"])
def messages():

    if request.method == "GET":
        messages = [message.to_dict() for message in Message.query.all()]

        return make_response(messages, 200)

    elif request.method == "POST":
        new_message = Message(
            body=request.json["body"],
            username=request.json["username"],
        )

        db.session.add(new_message)
        db.session.commit()

        new_message_dict = new_message.to_dict()

        return make_response(new_message_dict, 201)


@app.route("/messages/<int:id>", methods=["GET", "PATCH", "DELETE"])
def messages_by_id(id):
    if request.method == "GET":
        message = Message.query.filter_by(id=id).first()
        message_dict = message.to_dict()
        return make_response(message_dict, 200)

    elif request.method == "PATCH":
        message = Message.query.filter_by(id=id).first()
        message.body = request.json["body"]
        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()
        return make_response(message_dict, 200)

    elif request.method == "DELETE":
        message = Message.query.filter_by(id=id).first()
        db.session.delete(message)
        db.session.commit()

        return make_response("", 204)


if __name__ == "__main__":
    app.run(port=5555)
