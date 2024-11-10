from pydantic import BaseModel


class Notation(BaseModel):
    character_name: str
    notation: str
    draw_starter_frame: bool | None = True


class Movetable(BaseModel):
    character_name: str


class Findmove(BaseModel):
    character_name: str
    notation: str | None = ""
    name_move: str | None = ""
