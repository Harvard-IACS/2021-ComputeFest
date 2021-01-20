import os
import random
import pandas as pd
from fastapi import APIRouter, Path, Query
import torch
from torch.cuda import amp
from transformers import GPT2Config, GPT2DoubleHeadsModel, GPT2Tokenizer

import serving.utils as serving_utils
from  serving.routers import model_utils

router = APIRouter()

trained_model_path = os.path.join(serving_utils.DATASET_PATH,"trained_model")
model = None
tokenizer = None
dogs_memos = None

def get_model_tokenizer():
    global model
    global tokenizer
    if model is None:
        # Load trained model
        model = GPT2DoubleHeadsModel.from_pretrained(trained_model_path)
        # Convert model parameter tensors to device
        model.to("cpu")
        # Load trained Tokenizer
        tokenizer = GPT2Tokenizer.from_pretrained(trained_model_path)

    return model, tokenizer

def get_dog_memos():
    global dogs_memos
    if dogs_memos is None:
        dogs_website_memos_path = os.path.join(serving_utils.DATASET_PATH, "dog_data_small", "dogs_website_memos.csv")
        with open(dogs_website_memos_path, 'r') as file:
            dogs_website_memos = file.read()

        dogs_website_memos = dogs_website_memos.replace('\n\n', '')
        dogs_website_memos = dogs_website_memos.replace('\n \n', '')
        dogs_website_memos = dogs_website_memos.replace('"\n', '"<EOL>')
        dogs_website_memos = dogs_website_memos.replace('\\"', '')
        dogs_website_memos = dogs_website_memos.replace('\n', '')
        dogs_website_memos = dogs_website_memos.replace('<EOL>', '\n')
        dogs_website_memos = [row for row in dogs_website_memos.split(sep='\n')]
        dogs_website_memos = dogs_website_memos[1:]  # Remove header
        dogs_website_memos = dogs_website_memos[:-1]  # Remove last empty row

        dogs_memos = []
        for row in dogs_website_memos:
            dogs_memos.append({
                "AnimalInternalID": int(row.split(',"')[0]),
                "MemoText": row.split(',"')[1]
            })
        dogs_memos = pd.DataFrame(dogs_memos)
        print("Shape:", dogs_memos.shape)
        print(dogs_memos.head())

    return dogs_memos

def generate_persona(dog_data):
    house_trained = random.randint(0, 3)
    if house_trained == 0:
        dog_data["trained"] = False
    else:
        dog_data["trained"] = True

    personality = ['My name is {}.'.format(dog_data["AnimalName"]),
    'I am a {}.'.format(dog_data["AnimalType"]),
    'My gender is {}.'.format(dog_data["AnimalSex"]),
    'My weight is {}.'.format(dog_data["AnimalCurrentWeightPounds"]),
    'I was born on {}.'.format(dog_data["Year"]),
    'I am {} years old.'.format(dog_data["Age"]),
    'My age is {}.'.format(dog_data["Age"]),
    'My breed is {}.'.format(dog_data["AnimalBreed"]),
    'My color is {}.'.format(dog_data["AnimalColor"]),
    ]

    if dog_data["trained"]:
        personality.append("I am house trained")
    else:
        personality.append("I am not house trained")

    return personality

@router.post(
    "/chat_with_dog",
    summary="Get dialog model prediction for the dog",
    description="Get dialog model prediction for the dog"
)
async def chat_with_dog(
        chat: dict
):
    print("chat", chat)

    # Get model/ tokenizer
    model, tokenizer = get_model_tokenizer()
    dogs_memos = get_dog_memos()

    memo = dogs_memos[dogs_memos["AnimalInternalID"]== int(chat["dog"]["AnimalInternalID"])]["MemoText"].values
    print(memo)

    personality = generate_persona(chat["dog"])

    if len(memo) > 0:
        memo = memo[0].replace("\"","")
        memo = memo.split(". ")
        if len(memo) > 6:
            memo = memo[:6]
        personality.extend(memo)
    else:
        memo = [
            "I have the prettiest little puppy face.",
            "I am sweet.",
            "I have stunning grey eyes that will win you over instantly, and have the cutest floppy ears.",
            "I am still learning what my crate is for, and working hard to master house training.",
            "I love crinkly stuffed toys.",
            "I am very low key and relaxed.",
            "I love to be held, and will cuddle in your lap to take a snooze.",
        ]
        personality.extend(memo)
    # History
    history = chat["history"]
    # New chat message
    input_message = chat["input_message"]

    print("personality",personality)
    print("history",history)
    print("input_message",input_message)

    # Tokenize inputs
    personality = [tokenizer.encode(s.lower()) for s in personality]
    history = [tokenizer.encode(s) for s in history]
    history.append(tokenizer.encode(input_message))

    with torch.no_grad():
        with amp.autocast():
            out_ids = model_utils.sample_sequence(personality, history, tokenizer, model)
    out_text = tokenizer.decode(out_ids, skip_special_tokens=True)
    print("out_text",out_text)

    return {
        "response_message": out_text
    }