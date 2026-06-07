from dotenv import load_dotenv
from openai import OpenAI
import os
import base64

from prompts.prompts import SYSTEM_PROMPT

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

print("OPENAI_API_KEY FOUND:", api_key is not None)

client = OpenAI(
    api_key=api_key
)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


def ask_image_question(image_path, question):

    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": question
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url":
                            f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500
    )

    return response.choices[0].message.content