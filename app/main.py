from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from .model import Notation
from PIL import Image
import io, re

app = FastAPI()


def convert_notation(data: str):
    # Replace symbols with words
    data = data.replace(" ", "(next)")
    data = data.replace(":", "(colon)")
    data = data.replace("*", "(hold)")
    data = data.replace("<", "(delay1)")
    data = data.replace(">", "(delay2)")

    # Convert capital letters to the format ^lowercase
    data = re.sub(r"([A-Z])", lambda match: f"^{match.group(1).lower()}", data)
    return data


def draw_notation(notation: list):
    images = []
    for raw in notation:
        try:
            processed = convert_notation(raw)
            img = Image.open(f"./app/public/button/{processed}.png")
            images.append(img)
        except FileNotFoundError:
            return {"error": f"Notation '{raw}' not found."}
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
    results = draw_notation(data.notation.split(","))
    if isinstance(results, dict):
        return results
    img_byte_array = io.BytesIO()
    results.save(img_byte_array, format="JPEG")
    img_byte_array.seek(0)
    return StreamingResponse(img_byte_array, media_type="image/jpeg")
