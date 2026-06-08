#Loads trained model + sets up Gemma 3 model pipeline + tests Gemma 3's text generalization skills

from transformers import pipeline #easy access to NLP models
from ultralytics import YOLO #ultralytics library providing YOLO model for obj detection

#load our trained model
#TODO: update the path to the model once we trained it with more epochs for better accuracy
model = YOLO('best.pt')

#loading gemma 3
generator = pipeline( #specify the task (text-gen) and model we want to use for text generation
    task = "text-generation",
    model = "google/gemma-3-1b-it",
)

#TEST GEMMA 3'S TEXT GENERALIZATION SKILLS (COMMENT OUT LATER ON!)

# occasion = "beach day"
# wardrobe_text = """
# - Item 1: white linen shirt
# - Item 2: navy chinos
# - Item 3: brown sandals
# """

# prompt = f"""<start_of_turn>user
# You are a fashion stylist.
# Occasion: {occasion}
# Wardrobe: {wardrobe_text}
# Return 3 outfits as JSON.
# <end_of_turn>
# <start_of_turn>model
# """

# response = generator(
#     prompt,
#     max_new_tokens=300,
#     do_sample=True,
#     temperature=0.7
# )

# print(response[0]['generated_text'])