"""In-memory session auth for WeChat mini-program ship gate (Z0).

Production: set WECHAT_APP_ID / WECHAT_APP_SECRET and AUTH_REQUIRED=true.
Local/CI: AUTH_DEV_LOGIN=true accepts any code and issues a Bearer token.
"""

from __future__ import annotations

import hashlib
import secrets
import time
from dataclasses import dataclass, field

import httpx

from app.core.config import settings


@dataclass
class SessionUser:
    user_id: str
    openid: str
    created_at: float = field(default_factory=time.time)
    deleted: bool = False


_sessions: dict[str, SessionUser] = {}
_deleted_openids: set[str] = set()


def clear_sessions_for_tests() -> None:
    _sessions.clear()
    _deleted_openids.clear()


def _token() -> str:
    return secrets.token_urlsafe(32)


async def exchange_wechat_code(code: str) -> str:
    """Return openid. Dev login synthesizes openid when secrets missing."""
    if settings.auth_dev_login and (
        not settings.wechat_app_id or not settings.wechat_app_secret or code.startswith("dev")
    ):
        digest = hashlib.sha256(code.encode("utf-8")).hexdigest()[:16]
        return f"dev_openid_{digest}"

    if not settings.wechat_app_id or not settings.wechat_app_secret:
        raise RuntimeError("未配置 WECHAT_APP_ID/SECRET，且 AUTH_DEV_LOGIN 未开启")

    url = "https://api.weixin.qq.com/sns/jscode2session"
    params = {
        "appid": settings.wechat_app_id,
        "secret": settings.wechat_app_secret,
        "js_code": code,
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url, params=params)
        data = resp.json()
    if data.get("errcode"):
        raise RuntimeError(f"微信登录失败: {data.get('errmsg') or data}")
    openid = data.get("openid")
    if not openid:
        raise RuntimeError("微信登录未返回 openid")
    return str(openid)


async def login(code: str) -> dict:
    openid = await exchange_wechat_code(code)
    if openid in _deleted_openids:
        _deleted_openids.discard(openid)
    user_id = f"u_{hashlib.sha256(openid.encode()).hexdigest()[:12]}"
    access = _token()
    _sessions[access] = SessionUser(user_id=user_id, openid=openid)
    return {
        "access_token": access,
        "token_type": "bearer",
        "expires_in": settings.session_ttl_seconds,
        "user_id": user_id,
    }


def get_session(token: str | None) -> SessionUser | None:
    if not token:
        return None
    user = _sessions.get(token)
    if user is None or user.deleted:
        return None
    if time.time() - user.created_at > settings.session_ttl_seconds:
        _sessions.pop(token, None)
        return None
    return user


def logout(token: str | None) -> bool:
    if not token:
        return False
    return _sessions.pop(token, None) is not None


def delete_account(token: str | None) -> bool:
    user = get_session(token)
    if user is None:
        return False
    _deleted_openids.add(user.openid)
    # drop all sessions for this openid
    dead = [k for k, v in _sessions.items() if v.openid == user.openid]
    for k in dead:
        _sessions.pop(k, None)
    return True
