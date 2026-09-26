from pydantic import BaseModel, HttpUrl


class URLCreate(BaseModel):
    longurl: HttpUrl
