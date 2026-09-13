from pydantic import BaseModel, Field


class AuthLoginRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=128, description="wx.login code 或 dev 测试码")


class AuthLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: str


class AuthMeResponse(BaseModel):
    user_id: str
    openid_masked: str
