from flask import Flask, request
from db import db
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os
import json
from transformers import pipeline
from ultralytics import YOLO
from db import Piece
from PIL import Image
import io

load_dotenv() #loads sensitive varible infor from .env file

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)

cvmodel = YOLO('best.pt')

generator = pipeline(
    task = "text-generation",
    model = "google/gemma-3-1b-it",
)

app = Flask(__name__)
db_filename = "game.db"

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///closet-db"
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
#addClothes()
@app.route("/wardrobe/", methods=["POST"])
def addClothes():
    #take in image
    if not request.data:
        return failure_response("no image provided", 400)
    image_bytes=request.data #multiform request: json string+files, flask auto stores as FileStorage object
    
    image_stream=io.BytesIO(image_bytes)
    img=Image.open(image_stream)
    
    print(type(img))
    #store that in cloud database
    upload_result=cloudinary.uploader.upload(image_bytes) #should we save individual images?
    image_url=upload_result["secure_url"]
    #add to wardrobe inventory
    results=cvmodel(img, save_crop=True) #saves all cropped images in subfolder called crop
    #only 1 image so results[0] will give first one
    pieces=[]
    print("hi", len(results[0].boxes.cls))
    for obj in results[0].boxes.cls: #each reprpesetns one detected object in image
        piece=Piece(label=obj.item(), image=image_url, color="unknown") #.item() converts tensor of classID to plain number
        db.session.add(piece)
        db.session.commit()
        pieces.append(piece.serialize())

    return success_response(pieces, 201)


#removeClothingItem()
@app.route("/wardrobe/<int:id>", methods=["DELETE"])
def removeClothingItem(id):
    item=Piece.query.get(id)
    if item is None:
        return failure_response("Id is not valid")
    db.session.delete(item)
    db.session.commit()
    return success_response(item.serialize())

@app.route("/wardrobe/outfit/", methods=["GET"])
def getOutfit():
    body=json.loads(request.data)
    filters=body.get("filters") #sent in as json of json (weather, occassion, color as keys")
    if filters is None:
        return failure_response("filters were not given")
    pieces = Piece.query.all()
    wardrobe_txt = ""
    for piece in pieces:
        wardrobe_txt +=f"- Item {piece.id}: {piece.color} {piece.label}\n"

    prompt = f"""<start_of_turn>user
    You are a fashion stylist.
    CONTEXT:
    -Weather: {filters.get('weather', 'mild')}
    -Occasion: {filters.get('occasion', 'casual')}
    -Color preference: {filters.get("color", "not specified")}
    AVAILABLE WARDROBE (use ONLY these items, referenced by their ID):
    {wardrobe_txt}

    TASK:
    Generate exactly 3 complete outfits using only items from the wardrobe above.

    RULES:
    - Every outfit must be appropriate for the weather, occasion, and color preference
    - Do not repeat the same combination across outfits
    - Each outfit must include at least a top and a bottom
    - Prioritize color coordination and pattern balance
    - If color preference is specified, at least one item per outfit must match it

    RESPOND ONLY in this exact JSON format, no extra text:
    {{
    "outfits": [
        {{
        "outfit_number": 1,
        "items": [item_id_1, item_id_2, item_id_3],
        "description": "brief explanation of why this works",
        "why_it_fits_filters": "explain how it matches weather, occasion, color"
        }}
    ]
    }}
    """

    response = generator(
        prompt,
        max_new_tokens=300,
        do_sample=True,
        temperature=0.7
    )

    return {"response": response[0]['generated_text']}, 400



@app.route("/wardrobe/<int:id>", methods=["GET"])
def getClothingItem(id):
    item=Piece.query.get(id)
    if item is None:
        return failure_response("Id is not valid")
    return success_response(item.serialize())


@app.route("/wardrobe/", methods=["GET"])
def getWardrobe(): #return a  list
    wardrobe=[]
    for item in Piece.query.all():
        wardrobe.append(item.serialize())
    return {"wardrobe": wardrobe}, 200


#finsih entire thing +
#ItemClass.query=refers to your table
#200=success error code
#db.session: like an art tool to do stuff to dattabase (putting edits to be amd ein staging area)
#tensor?

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


