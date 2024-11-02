from pydantic import BaseModel


class Notation(BaseModel):
    character_name: str
    starter_frame: int
    notation: str
