from typing import Annotated

from fastapi import Depends, Header, HTTPException

from app.core.config import settings
from app.services import auth_service
from app.services.auth_service import SessionUser


def _bearer_token(authorization: str | None) -> str | None:
    if not authorization:
        return None
    parts = authorization.split(None, 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1].strip() or None


async def get_current_user_optional(
    authorization: Annotated[str | None, Header()] = None,
) -> SessionUser | None:
    token = _bearer_token(authorization)
    return auth_service.get_session(token)


async def require_user(
    authorization: Annotated[str | None, Header()] = None,
) -> SessionUser:
    """Enforce auth when AUTH_REQUIRED=true; otherwise return anonymous stub."""
    token = _bearer_token(authorization)
    user = auth_service.get_session(token)
    if user is not None:
        return user
    if not settings.auth_required:
        return SessionUser(user_id="anonymous", openid="anonymous")
    raise HTTPException(status_code=401, detail="未登录或令牌无效，请先调用 /auth/login")


async def get_request_id(x_request_id: Annotated[str | None, Header()] = None) -> str | None:
    return x_request_id


CurrentUser = Annotated[SessionUser, Depends(require_user)]
