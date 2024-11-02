from pydantic import BaseModel


class Notation(BaseModel):
    character_name: str | None = None
    starter_frame: int
    notation: str


class Movetable(BaseModel):
    character_name: str
