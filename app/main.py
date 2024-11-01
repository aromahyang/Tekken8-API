from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from .model import Notation
from PIL import Image
import io, re

app = FastAPI()


def convert_notation(data: str):
    data = data.replace(" ", ",(next),")
    data = data.replace(":", ",(colon),")
    data = data.replace("*", ",(hold),")
    data = data.replace("<", ",(delay1),")
    data = data.replace(">", ",(delay2),")
    data = re.sub(r"([A-Z])", lambda match: f"^{match.group(1).lower()}", data)
    return data


def draw_notation(notation: list):
    images = []
    for file_name in notation:
        try:
            img = Image.open(f"./app/public/button/{file_name}.png")
            images.append(img)
        except FileNotFoundError:
            return {"error": f"Notation '{file_name}'."}
    if not images:
        return {"error": "No images to merge."}

    new_width = sum(img.width for img in images)
    new_height = max(img.height for img in images)
    new_image = Image.new("RGB", (new_width, new_height))

    current_x = 0
    for img in images:
        new_image.paste(img, (current_x, 0))
        current_x += img.width

    return new_image


@app.post("/notation")
async def notation(data: Notation):
    n = convert_notation(data.notation)
    new_image = draw_notation(n.split(","))
    if isinstance(new_image, dict):
        return new_image
    img_byte_array = io.BytesIO()
    new_image.save(img_byte_array, format="JPEG")
    img_byte_array.seek(0)
    return StreamingResponse(img_byte_array, media_type="image/jpeg")
