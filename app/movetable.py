from bs4 import BeautifulSoup
from .model import Movetable, Findmove
from difflib import get_close_matches
import requests, re


# Converting for searching moveset
def convert_moveset(move: str):
    move = move.replace("WR", "f,f,F+")
    move = move.replace("wr", "f,f,F+")
    move = move.replace("WS", "ws")
    move = move.replace("ewgf", "f,n,d,df+2")
    move = move.replace("RA", "R.df+1+2")
    move = move.replace("HS", "H.2+3")
    move = move.replace("HB", "2+3")
    return move


async def finding_similiar_move(param: Findmove):
    # Makro for character name
    if param.character_name == "DVJ" or param.character_name == "dvj":
        param.character_name = "Devil Jin"
    data = await get_movetable(Findmove(character_name=param.character_name))
    param.notation = convert_moveset(param.notation)

    if param.notation:
        moveset_matches = get_close_matches(
            param.notation,
            [
                item["moveset"].replace(f"{param.character_name.title()}-", "")
                for item in data
            ],
            n=5,
            cutoff=0.6,
        )
        filtered_result = [
            item
            for item in data
            if item["moveset"].replace(f"{param.character_name.title()}-", "")
            in moveset_matches
        ]
    elif param.name_move:
        closest_name_move = get_close_matches(
            param.name_move.title(),
            [item["name_move"] for item in data],
            n=5,
            cutoff=0.6,
        )
        filtered_result = [
            item for item in data if item["name_move"] in closest_name_move
        ]
    return (
        filtered_result
        if filtered_result
        else {"error": "No matching moveset found", "param": param}
    )


async def finding_move(param: Findmove):
    # Makro for character name
    if param.character_name == "DVJ" or param.character_name == "dvj":
        param.character_name = "Devil Jin"

    data = await get_movetable(Findmove(character_name=param.character_name))
    param.notation = convert_moveset(param.notation)
    # If notation is provided, perform an exact match on "moveset"
    if param.notation:
        if "stance" in param.notation:
            # Get value inside parentheses in "stance(...)" and store that value
            stance = re.search(r"\((.*?)\)", param.notation).group(1)
            # Change text stance(...) in param.notation to variabel stance previously created
            param.notation = param.notation.replace(f"stance({stance})", stance)

            # Split converted_move with comma (,)
            converted_moves = param.notation.split(",")
            # And search the value in raw_data with conditions if len(converted_moves) == raw_data["moveset"]
            filtered_result = [
                item
                for item in data
                if all(
                    move
                    in item["moveset"]
                    .replace(f"{param.character_name.title()}-", "")
                    .split(",")
                    and len(
                        item["moveset"]
                        .replace(f"{param.character_name.title()}-", "")
                        .split(",")
                    )
                    == len(converted_moves)
                    for move in converted_moves
                )
            ]
        else:
            target_moveset = f"{param.character_name.title()}-{param.notation}"
            # Search value target in raw_data
            filtered_result = [
                item for item in data if item["moveset"] == target_moveset
            ]
    elif param.name_move:
        name_move_target = param.name_move.title()
        name_filtered = get_close_matches(
            name_move_target,
            [item["name_move"] for item in data],
            n=10,
            cutoff=0.6,
        )
        filtered_result = [item for item in data if item["name_move"] in name_filtered]

    # Return filtered results or an error if none found
    return (
        filtered_result
        if filtered_result
        else {"error": "No matching moveset found", "param": param}
    )


async def get_starter_frame(character_name: str, notation: str):
    # Makro for character name
    if character_name == "DVJ" or character_name == "dvj":
        character_name = "Devil Jin"

    notation = notation.replace(".", ",")
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


async def get_version():
    url = f"https://wavu.wiki/t/Main_Page"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        raw = soup.find(class_="floatright")
        result = [data for data in raw.get_text().split("\n") if "Version" in data]
        return result
    else:
        return {"error": "error while getting version"}


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

        # Get raw data
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
        # Process raw data
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
        return result
    else:
        return {"error": "error while getting frame data"}
