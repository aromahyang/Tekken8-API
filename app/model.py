from pydantic import BaseModel


class Notation(BaseModel):
    frame: int
    notation: str
