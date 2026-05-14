from typing import Annotated

from fastapi import Depends, Header


async def get_request_id(x_request_id: Annotated[str | None, Header()] = None) -> str | None:
    return x_request_id

