from pydantic import BaseModel


class Issue(BaseModel):
    fname: str
    line_start: int
    line_end: int
    content: str
