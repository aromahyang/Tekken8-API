from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from .model import Notation
from .notation import get_img_notation
import io

app = FastAPI()


@app.post("/notation")
async def notation(data: Notation):
    notation_img = get_img_notation(data)
    img_byte_array = io.BytesIO()
    notation_img.save(img_byte_array, format="JPEG")
    img_byte_array.seek(0)
    return StreamingResponse(img_byte_array, media_type="image/jpeg")
