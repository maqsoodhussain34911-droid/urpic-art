import base64
from openai import OpenAI
from PIL import Image
import io

def convert_to_sketch(api_key, image_path):
    client = OpenAI(api_key=api_key)

    with open(image_path, "rb") as img:
        response = client.images.edit(
            model="gpt-image-1",
            image=img,
            prompt="Convert this into a detailed pencil sketch",
            size="1024x1024"
        )

    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    return Image.open(io.BytesIO(image_bytes))