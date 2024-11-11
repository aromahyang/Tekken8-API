from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from .model import Notation, Movetable, Findmove
from .notation import get_img_notation
from .movetable import get_movetable, finding_move, finding_similiar_move, get_version
import io

app = FastAPI()


@app.get("/")
async def movetable():
    result = await get_version()
    return {"detail": "Using" + result[0]} if "error" not in result else result


@app.post("/movetable")
async def movetable(data: Movetable):
    result = await get_movetable(data)
    return {"total_data": len(result), "data": result}


@app.post("/findmove")
async def findmove(data: Findmove):
    main_result = await finding_move(data)
    similiar = await finding_similiar_move(data)
    return {
        "total_data": (
            len(main_result) if isinstance(main_result, list) else len(similiar)
        ),
        "data": main_result,
        "similiar": similiar,
    }


@app.post("/notation")
async def notation(data: Notation):
    notation_img = await get_img_notation(data)
    if isinstance(notation_img, dict):
        return notation_img
    img_byte_array = io.BytesIO()
    notation_img.save(img_byte_array, format="PNG")
    img_byte_array.seek(0)
    return StreamingResponse(img_byte_array, media_type="image/png")
