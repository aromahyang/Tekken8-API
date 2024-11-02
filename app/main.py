from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from .model import Notation, Movetable
from .notation import get_img_notation
from bs4 import BeautifulSoup
import io, requests

app = FastAPI()


@app.post("/movetable")
async def movetable(data: Movetable):
    url = f"https://wavu.wiki/t/{data.character_name}_movetable"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        def get_data(classname: str):
            raw = soup.find_all(class_=classname)
            result = [data.get_text(strip=True) for data in raw]
            return result

        raw = {
            "moveset": get_data("field_Move"),
            "startup": get_data("field_Startup"),
            "hit_properties": get_data("field_Hit_Level"),
            "damage": get_data("field_Damage"),
            "on_block": get_data("field_On_Block"),
            "on_hit": get_data("field_On_Hit"),
            "on_CH": get_data("field_On_CH"),
            "states": get_data("field_States"),
            "notes": get_data("field_Notes"),
        }
        result = [
            {
                "moveset": raw["moveset"][i],
                "startup": raw["startup"][i],
                "hit_properties": raw["hit_properties"][i],
                "damage": raw["damage"][i],
                "on_block": raw["on_block"][i],
                "on_hit": raw["on_hit"][i],
                "on_CH": raw["on_CH"][i],
                "states": raw["states"][i],
                "notes": raw["notes"][i],
            }
            for i in range(len(raw["moveset"]))
            if raw["moveset"][i] != "Move"
        ]
        return {"data": result}
    else:
        return {"error": "error while getting frame data"}


@app.post("/notation")
async def notation(data: Notation):
    notation_img = get_img_notation(data)
    if isinstance(notation_img, dict):
        return notation_img
    img_byte_array = io.BytesIO()
    notation_img.save(img_byte_array, format="JPEG")
    img_byte_array.seek(0)
    return StreamingResponse(img_byte_array, media_type="image/jpeg")
