import string
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from .database import URLDatabase
from .models import URLCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- startup ----
    app.state.db = URLDatabase()
    print("Database connected")

    yield  # app runs here, handling requests

    # ---- shutdown ----
    app.state.db.close()
    print("Database closed")


app = FastAPI(lifespan=lifespan)

BASE_URL = "http://127.0.0.1:8000"


def makeshorturl(num):
    charbase = string.digits + string.ascii_uppercase + string.ascii_lowercase
    if num == 0:
        return charbase[0]
    _char = []
    _base = len(charbase)
    while num > 0:
        num, remainder = divmod(num, _base)
        _char.append(charbase[remainder])
    return "".join(reversed(_char))


@app.post("/url")
def geturl(longurl: URLCreate, request: Request):
    db: URLDatabase = request.app.state.db
    long_url = str(longurl.longurl)

    if db.long_url_exists(long_url):
        return {"shorturl": f"{BASE_URL}/{db.get_short_code_by_long_url(long_url)}"}
    else:
        n = db.insert_url(long_url)
        shorturl = makeshorturl(n)
        db.set_short_code(n, shorturl)
        return {"shorturl": f"{BASE_URL}/{shorturl}"}


from fastapi import HTTPException
from fastapi.responses import RedirectResponse


@app.get("/{short_code}")
def redirect(short_code: str, request: Request):
    db: URLDatabase = request.app.state.db

    entry = db.get_by_code(short_code)

    if not entry:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return RedirectResponse(url=entry["long_url"], status_code=302)
