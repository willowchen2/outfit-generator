from flask import Flask, request
from db import db

app = Flask(__name__)
db_filename = "game.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False  # set to True to log SQL queries while debugging

db.init_app(app)
with app.app_context():
    db.create_all()

# Response helpers 
def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

#routes
#addImages()
@app.route("/wardrobe/", methods=["POST"])
def addImage():
    pass

#resetInventory()
#removeImages()
#getOutfit()




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


