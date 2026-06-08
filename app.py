import cloudinary
import cloudinary.uploader

from flask import Flask, request, jsonify
from flask.cli import load_dotenv 
from db import db, Piece
from main import model, generator #import the AI models
from flask_cors import CORS #cross origin resource sharing, disables default restriction that blocks front & backend comms

import json
import os

app = Flask(__name__) #create Flask web server object
CORS(app) #enable cross origin resource sharing btwn front & backend

#LATER we will move from local to cloud via os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/closet_db"
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


#cloudinary config
load_dotenv() #loads sensitive varible infor from .env file

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)


#routes
@app.route("/")
def home():
    return success_response("Welcome to the closet API!")

#addClothing so basically call upload_image()
@app.route("/wardrobe/", methods=["POST"])
def addClothing():
    img = request.files.get("image")
    if img is None:
        return failure_response("No image provided", code=400)
    
    #upload directly to cloudinary and get the URL
    upload_result = cloudinary.uploader.upload(img,folder = "wardrobe_pieces") #the folder param organizes images in cloudinary account
    img_url = upload_result['secure_url']



    results=model(img, save_crop=True) #saves all cropped images in subfolder called crop
    #only 1 image so results[0] will give first one
    for obj in results[0].boxes.cls: #each reprpesetns one detected object in image
        piece=Piece(obj.item(), img_url, "unknown") #.item() converts tensor of classID to plain number
        db.session.add(piece)
        db.session.commit()


    return success_response(piece.to_dict(), 201)

    # #save the image URL and label following yolo processing
    # results = model(img_url) #call YOLO model
    # label = results[0].names[results[0].boxes.cls[0].item()] #get the label of the detected clothing item from YOLO results

    # #make a new Piece object and add it to the database 
    # piece = Piece(label=label, color = "unknown",image=img_url) #EDIT LATER TO INCLUDE COLOR
    # db.session.add(piece)
    # db.session.commit()

    # return success_response(piece.to_dict(), code=201)


#getClothing item in wardrobe
@app.route("/wardrobe/", methods=["GET"])
def getWardrobe():
    pieces = Piece.query.all()
    dict = []
    for piece in pieces:
        dict.append(piece.to_dict())
    return success_response(dict, code=200) 


@app.route("/wardrobe/<int:id>", methods=["GET"])
def getClothingItem(id):
    piece = Piece.query.get(id)
    if piece is None:
        return failure_response("Clothing item not found", code=404)
    return success_response(piece.to_dict(), code=200)


@app.route("/wardrobe/<int:id>", methods=["DELETE"])
def removeClothingItem(id):
    piece = Piece.query.get(id)
    if piece is None:
        return failure_response("Clothing item not found", code=404)
    
    db.session.delete(piece)
    db.session.commit()
    return success_response("Clothing item removed", code=200)

@app.route("/outfit/", methods=["POST"])

#getOutfit()
@app.route("/wardrobe/outfit/", methods=["GET"])
def getOutfit():
    pieces = Piece.query.all()
    wardrobe_txt = ""
    for piece in pieces:
        wardrobe_txt +=f"- Item {piece.id}: {piece.color} {piece.label}\n"
    body = json.loads(request.data) #loads JSON data and converts into a dictionary
    occasion = body.get("occasion")
    weather = body.get("weather","mild")
    color = body.get("color","no preference")


    prompt = """You are an expert fashion stylist with deep knowledge of color theory, pattern mixing, and occasion dressing.
    
    Context:
    Occasion: {occasion}
    Weather: {weather}
    Color preference: {color}
    Available wardrobe: {wardrobe_txt}

    TASK:
    Generate exactly 3 complete outfits using only items from the wardrobe above.

    RULES:
    - Every outfit must be appropriate for the weather, occasion, and color preference
    - Do not repeat the same combination across outfits
    - Each outfit must include at least a top and a bottom
    - Prioritize color coordination and pattern balance
    - If color preference is specified, at least one item per outfit must match it

    Respond in JSON format as follows:
    {{
    "stylist notes": "brief explanation of the outfit choices and how they fit the occasion/weather/color preference",
    "outfits": [
        {{
        "outfit_name": "name of the outfit",
        "selected_ids": [1,4],
        ""description": "detailed description of the outfit, including how the pieces work together and why they are suitable for the occasion"
        }},
        {{
        "outfit_name": "name of the outfit",
        "selected_ids": [2,3],
        "description": "detailed description of the outfit, including how the pieces work together and why they are suitable for the occasion"
        }},
        {{
        "outfit_name": "name of the outfit",
        "selected_ids": [5,6],
        "description": "detailed description of the outfit, including how the pieces work together and why they are suitable for the occasion"
        }}
    ]
    }}
             
    """




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


