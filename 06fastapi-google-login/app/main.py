import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.config import Config


app = FastAPI()
config = Config(".env")
oauth = OAuth(config)
secret_key = config("SECRET_KEY")

app.add_middleware(SessionMiddleware, secret_key=secret_key)



CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={
        "scope": "openid email profile"
    },
)

@app.get("/")
async def homepage(request: Request):
    user = request.session.get("user")
    if user:
        data = json.dumps(user, indent=4)
        html = f"""
        <pre>{data}</pre>
        <a href="/logout">Logout</a>
        """
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">Login with Google</a>')

@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    print(redirect_uri,request)
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth")
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user = token.get("userinfo")
        if user:
            request.session["user"] = dict(user)
        return RedirectResponse(url="/")
    except OAuthError as error:
        return HTMLResponse(f"<h1>Authentication Error: {error.error}</h1>")

@app.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")
