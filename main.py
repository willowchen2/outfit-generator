from ultralytics import YOLO
from transformers import pipeline
import torch

model=YOLO('best.pt')

#use an llm pipeline that is a structure that presents raw data as processed valid input to the llm along witha ny other information like retrived context

generator=pipeline(
    task="text-generation",
    model="google/gemma-3-1b-it",
    #torch_dtype=torch.float16, #use fp16
    #device_map="auto" #automatically ahndles hardware sharing
)

occasion = "beach day"
wardrobe_text = """
- Item 1: white linen shirt
- Item 2: navy chinos
- Item 3: brown sandals
"""

prompt=f"""
    You are a fashion stylist.
    Occasion: {occasion}
    Wardrobe: {wardrobe_text}
    Return 3 outfits as a  json string.
"""

response=generator( #how does this format work?
    prompt,
    max_new_tokens=300,
    do_sample=True,
    temperature=0.7
)

print(response[0]['generated_text'])

#model should take in wardrobe and labels, output json string of outfit combos
