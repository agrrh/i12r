"""Issue object."""

from typing import Literal, Optional

from pydantic import BaseModel


class Issue(BaseModel):
    """Issue object."""

    fname: str
    line_start: Optional[int] = 0
    line_end: Optional[int] = 0
    level: Literal["TODO", "FIXME"]
    content: str
