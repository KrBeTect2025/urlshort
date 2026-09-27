import string
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from redis import Redis

from .database import URLDatabase
from .models import URLCreate


@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.db = URLDatabase()
    app.state.cache = Redis(host="localhost", port=6379, decode_responses=True)
    print("Database connected")
    print("redis connnected")

    yield

    app.state.db.close()
    print("Database closed")
    print("Redis is closed")


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
    cache: Redis = request.app.state.cache
    long_url = str(longurl.longurl)

    if db.long_url_exists(long_url):
        return {"shorturl": f"{BASE_URL}/{db.get_short_code_by_long_url(long_url)}"}
    else:
        n = db.insert_url(long_url)
        shorturl = makeshorturl(n)
        db.set_short_code(n, shorturl)
        cache.set(shorturl, long_url, ex=3600)
        return {"shorturl": f"{BASE_URL}/{shorturl}"}


from fastapi import HTTPException
from fastapi.responses import RedirectResponse


@app.get("/{short_code}")
def redirect(short_code: str, request: Request):
    db: URLDatabase = request.app.state.db
    cache: Redis = request.app.state.cache
    long_url = cache.get(short_code)
    print("CACHE HIT" if long_url else "CACHE MISS")

    if not long_url:
        entry = db.get_by_code(short_code)
        if not entry:
            raise HTTPException(status_code=404, detail="short url arent found")
        long_url = entry["long_url"]
        assert isinstance(long_url, str)
        cache.set(short_code, long_url, ex=3600)

    assert isinstance(long_url, str)
    return RedirectResponse(url=long_url, status_code=302)
