from datetime import datetime

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import const
import rdb_crud
import rdb_models
from rdb import SessionLocal, engine

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
rdb_models.Base.metadata.create_all(bind=engine)


def get_rdb_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_rdb_session)):
    books = rdb_crud.get_books(db)
    timestamp = datetime.now(const.JST).isoformat()[0:23]  # 日本時間のミリ秒3桁までの文字列

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "timestamp": timestamp,
            "books": books,
        }
    )


@app.post("/", response_class=HTMLResponse)
async def post(request: Request,
               db: Session = Depends(get_rdb_session),
               title: str = Form("")):
    if title is None or title == "":
        books = rdb_crud.get_books(db)
        timestamp = datetime.now(const.JST).isoformat()[0:23]  # 日本時間のミリ秒3桁までの文字列
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error_msg": "タイトルを入力してね 📝",
                "timestamp": timestamp,
                "books": books,
            }
        )

    rdb_crud.insert_books(db, title)
    books = rdb_crud.get_books(db)
    timestamp = datetime.now(const.JST).isoformat()[0:23]  # 日本時間のミリ秒3桁までの文字列

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "timestamp": timestamp,
            "books": books,
        }
    )

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
