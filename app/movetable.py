from bs4 import BeautifulSoup
from .model import Movetable
import requests, re


# For searching moveset
def convert_moveset(move: str):
    move = move.replace("WS", "ws")
    move = move.replace("ewgf", "f,n,d,df+2")
    move = move.replace("RA", "R.df+1+2")
    return move


async def find_move(character_name: str, notation: str):
    # Makro for character name
    if character_name == "DVJ" or character_name == "dvj":
        character_name = "Devil Jin"

    raw_data = await get_movetable(Movetable(character_name=character_name))
    if "error" in raw_data:
        return raw_data
    converted_move = convert_moveset(notation)

    # Split converted_move with spaces and get the first part if part have a digit (have action)
    converted_move = next(
        (part for part in converted_move.split(" ") if re.search(r"\d", part)), ""
    )
    if not converted_move:
        return {"error": "No move notation found", "character_name": character_name}

    # This condition if in notation using stance
    if "stance" in converted_move:
        # Get value inside parentheses in "stance(...)" and store that value
        stance = re.search(r"\((.*?)\)", converted_move).group(1)
        # Change text stance(...) in converted_move to variabel stance previously created
        converted_move = converted_move.replace(f"stance({stance})", stance)

        # Split converted_move with comma (,)
        converted_moves = converted_move.split(",")
        # And search the value in raw_data with conditions if len(converted_moves) == raw_data["moveset"]
        filtered_result = [
            item
            for item in raw_data
            if all(
                move
                in item["moveset"]
                .replace(f"{character_name.title()}-", "")
                .replace(".", ",")
                .split(",")
                and len(
                    item["moveset"]
                    .replace(f"{character_name.title()}-", "")
                    .replace(".", ",")
                    .split(",")
                )
                == len(converted_moves)
                for move in converted_moves
            )
        ]

    # If not using any stance in notation
    else:
        target_moveset = f"{character_name.title()}-{converted_move}"
        # Search value target in raw_data
        filtered_result = [
            item for item in raw_data if item["moveset"] == target_moveset
        ]

    return (
        filtered_result
        if filtered_result
        else {
            "error": f"No matching moveset found for {converted_move}",
            "character_name": character_name,
            "notation": notation,
        }
    )


async def get_movetable(data: Movetable):
    # Makro for character name
    if data.character_name == "DVJ" or data.character_name == "dvj":
        data.character_name = "Devil Jin"
    # Change name character if have spaces to + so url can be read
    url_character_name = data.character_name.replace(" ", "+")
    url = f"https://wavu.wiki/w/index.php?title=Special%3ACargoQuery&tables=Move&fields=CONCAT%28id%2C%27%27%29%3DMove%2Cname%3DNameMove%2Cstartup%3DStartup%2Ctarget%3DHit+Level%2Cdamage%3DDamage%2Cblock%3DOn+Block%2CCONCAT%28hit%2C%27%27%29%3DOn+Hit%2CCONCAT%28ch%2C%27%27%29%3DOn+CH%2Ccrush%3DStates%2Cnotes%3DNotes&where=Move._pageName%3D%27{url_character_name.title()}+movelist%27&join_on=&group_by=&having=&order_by%5B0%5D=&order_by_options%5B0%5D=ASC&limit=1000&offset=0&format=table"
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
            "name_move": get_data("field_NameMove"),
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
                "name_move": raw["name_move"][i],
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
        if not result:
            return {"error": f"No matching character found for {data.character_name}"}

        if data.notation is not None:
            filtered_result = [
                item
                for item in result
                if item["moveset"] == f"{data.character_name.title()}-{data.notation}"
            ]
            return (
                filtered_result[0]
                if filtered_result[0]
                else {"error": "No matching moveset found.", "data": result}
            )
        return result
    else:
        return {"error": "error while getting frame data"}
