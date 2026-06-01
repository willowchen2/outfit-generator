from transformers import pipeline
from ultralytics import YOLO

model = YOLO('best.pt')

generator = pipeline(
    task = "text-generation",
    model = "google/gemma-3-1b-it",

)

occasion = "beach day"
wardrobe_text = """
- Item 1: white linen shirt
- Item 2: navy chinos
- Item 3: brown sandals
"""



prompt = f"""<start_of_turn>user
You are a fashion stylist.
Occasion: {occasion}
Wardrobe: {wardrobe_text}
Return 3 outfits as JSON.
<end_of_turn>
<start_of_turn>model
"""

response = generator(
    prompt,
    max_new_tokens=300,
    do_sample=True,
    temperature=0.7
)

print(response[0]['generated_text'])