from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from .model import Notation, Movetable
from .notation import get_img_notation
from .movetable import get_movetable, find_move
import io

app = FastAPI()


@app.post("/findmove")
async def movetable(data: Movetable):
    result = await find_move(character_name=data.character_name, notation=data.notation)
    return {"total_data": len(result), "data": result}


@app.post("/movetable")
async def movetable(data: Movetable):
    result = await get_movetable(data)
    return {"total_data": len(result), "data": result}


@app.post("/notation")
async def notation(data: Notation):
    notation_img = await get_img_notation(data)
    if isinstance(notation_img, dict):
        return notation_img
    img_byte_array = io.BytesIO()
    notation_img.save(img_byte_array, format="JPEG")
    img_byte_array.seek(0)
    return StreamingResponse(img_byte_array, media_type="image/jpeg")
