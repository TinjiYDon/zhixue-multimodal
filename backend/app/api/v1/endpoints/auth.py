from fastapi import APIRouter, Header, HTTPException

from app.schemas.auth import AuthLoginRequest, AuthLoginResponse, AuthMeResponse
from app.services import auth_service

router = APIRouter()


def _bearer(authorization: str | None) -> str | None:
    if not authorization:
        return None
    parts = authorization.split(None, 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1].strip() or None


@router.post("/login", response_model=AuthLoginResponse)
async def login(body: AuthLoginRequest):
    try:
        result = await auth_service.login(body.code)
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return AuthLoginResponse(**result)


@router.post("/logout")
async def logout(authorization: str | None = Header(default=None)):
    auth_service.logout(_bearer(authorization))
    return {"status": "ok"}


@router.get("/me", response_model=AuthMeResponse)
async def me(authorization: str | None = Header(default=None)):
    user = auth_service.get_session(_bearer(authorization))
    if user is None:
        raise HTTPException(status_code=401, detail="未登录或令牌无效")
    return AuthMeResponse(user_id=user.user_id, openid_masked=user.openid[:6] + "***")


@router.delete("/me")
async def delete_me(authorization: str | None = Header(default=None)):
    """账号注销：使会话失效并标记 openid 已注销（B4）。"""
    ok = auth_service.delete_account(_bearer(authorization))
    if not ok:
        raise HTTPException(status_code=401, detail="未登录或令牌无效")
    return {"status": "deleted", "message": "账号已注销，本地会话已清除"}
