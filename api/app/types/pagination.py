from typing import Any

from pydantic import BaseModel


class Pagination(BaseModel):
    """ Pagination pydantic model"""
    total: int
    per_page: int
    current_page: int
    last_page: int
    data: list[Any]
