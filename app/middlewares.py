from starlette_context.middleware import RawContextMiddleware 
from starlette.requests import Request
from fastapi_jwt_auth import AuthJWT


class CustomContextMiddleware(RawContextMiddleware):
    async def set_context(self, request: Request):
        try:
            authorize = AuthJWT()
            authorize._get_jwt_from_headers(request.scope['headers'][6][1].decode())
            user_id = authorize.get_jwt_subject()
        except:
            user_id = None
        return {"user_id": user_id}