from PIL import Image, ImageFont, ImageDraw
from dotenv import load_dotenv
from .model import Notation
from .movetable import find_move
import re, os

load_dotenv()


def convert_notation(data: str):
    # Replace symbols with words
    data = data.replace("/", "")
    data = data.replace(" ", ",'next',")
    data = data.replace(".", ",")
    data = data.replace(":", ",'colon',")
    data = data.replace("*", ",'hold',")
    data = data.replace("<", ",'delay1',")
    data = data.replace(">", ",'delay2',")
    data = data.replace("WS", ",WS,")
    data = data.replace("~", ",~,")
    data = data.replace("[", "[,")
    data = data.replace("]", ",]")
    data = data.replace("F!", "FB!")

    # Add makro
    data = data.replace("qcf", "d,df,f")
    data = data.replace("qcb", "d,db,b")
    data = data.replace("hcf", "b,db,d,df,f")
    data = data.replace("hcb", "f,df,d,db,b")
    data = data.replace("dp", "f,d,df")
    data = data.replace("ewgf", "f,n,d,df,2")
    data = data.replace("RA", "R")
    data = data.replace("HB", "2+3,^h")

    # Convert capital letters to the format ^lowercase
    data = re.sub(r"([A-Z])", lambda match: f"^{match.group(1).lower()}", data)
    data = re.sub(r"([a-zA-Z]+)\+(\d+)", r"\1,\2", data)
    return data


def draw_character_name(name: str):
    font = ImageFont.truetype("arial.ttf", int(os.getenv("CHAR_NAME_FONT_SIZE")))
    raw_width = len(name) + 2
    img_size = (
        int(os.getenv("NAME_TEXT_WIDTH")) * raw_width,
        font.getbbox(name)[3] - font.getbbox(name)[1] + 32,
    )
    im = Image.new("RGBA", img_size)
    d = ImageDraw.Draw(im)
    d.text((0, 0), f"{name.title()}:", fill="white", font=font)
    return im


def draw_stances(name: str):
    font = ImageFont.truetype("arial.ttf", int(os.getenv("NOTATION_FONT_SIZE")) - 4)
    img_size = (
        int(font.getlength(" " + name + " ")),
        int(os.getenv("NOTATION_FONT_SIZE")),
    )
    im = Image.new("RGBA", img_size)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(
        [0, 0, im.width, im.height],
        radius=15,
        fill="white",
        outline="white",
    )
    d.text(
        (0, -8),
        f" {name} ",
        fill="black",
        font=font,
        align="center",
    )

    return im


def draw_starter_frame(frame_startup: str):
    font = ImageFont.truetype("arial.ttf", int(os.getenv("NOTATION_FONT_SIZE")))
    raw_width = int(font.getlength(frame_startup + "F "))
    img_size = (raw_width, int(os.getenv("NOTATION_FONT_SIZE")))
    im = Image.new("RGBA", img_size)
    d = ImageDraw.Draw(im)
    d.text((0, 0), f"{frame_startup}F", fill="white", font=font)
    return im


async def draw_notation(notation: list, data: Notation):
    images = []
    width_limit = int(os.getenv("IMAGE_NOTATION_WIDTH_LIMIT"))
    current_x = 0
    current_y = 0
    max_height_in_row = 0

    moveset = await find_move(data.character_name, data.notation)
    if "error" in moveset:
        starter_frame = "??"
    else:
        frame = re.findall(r"\d+", moveset[0]["startup"])
        starter_frame = f"{frame[0]}~{frame[1]}" if len(frame) > 1 else frame[0]
    img_frame = draw_starter_frame(starter_frame)
    images.append((img_frame, (current_x, current_y)))
    current_x += img_frame.width

    for raw in notation:
        if raw != "":
            try:
                if "stance" in raw:
                    stance = re.search(r"\((.*?)\)", raw).group(1)
                    stance = re.sub(
                        r"([a-z])", lambda match: f"{match.group(1).upper()}", stance
                    )
                    stance = stance.replace("^", "")
                    img = draw_stances(stance)
                else:
                    img = Image.open(f"./app/public/button/{raw}.png").convert("RGBA")

                img_width, img_height = img.size
                if current_x + img_width > width_limit:
                    current_x = 0
                    current_y += max_height_in_row + 10
                    max_height_in_row = img_height
                else:
                    max_height_in_row = max(max_height_in_row, img_height)

                images.append((img, (current_x, current_y)))
                current_x += img_width
            except FileNotFoundError:
                return {"error": f"Notation '{raw}' not found.", "data": notation}

    if not images:
        return {"error": "No images to merge."}
    new_width = width_limit
    new_height = current_y + max_height_in_row

    new_image = Image.new("RGBA", (new_width, new_height))
    for img, position in images:
        new_image.paste(img, position)

    return new_image


async def get_img_notation(data: Notation):
    if data.character_name == "DVJ" or data.character_name == "dvj":
        data.character_name = "Devil Jin"
    converted = convert_notation(data.notation)
    img_notation = await draw_notation(converted.split(","), data)
    if isinstance(img_notation, dict):
        return img_notation

    p = 5
    img_chara_name = draw_character_name(data.character_name)
    results = Image.new(
        "RGBA",
        (
            img_notation.width,
            img_notation.height + img_chara_name.height + p,
        ),
    )
    results.paste(img_chara_name, (0, 0))
    results.paste(img_notation, (0, img_chara_name.height + p))
    return results
