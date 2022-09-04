"""Issue object."""

from pydantic import BaseModel


class Issue(BaseModel):
    """Issue object."""

    fname: str
    line_start: int
    line_end: int
    content: str
