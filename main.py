from datetime import datetime

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import InternalError
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
            "aws_az": const.AWS_AZ,
            "private_ip": const.PRIVATE_IP,
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
                "aws_az": const.AWS_AZ,
                "private_ip": const.PRIVATE_IP,
                "error_msg": "タイトルを入力してね 📝",
                "timestamp": timestamp,
                "books": books,
            }
        )

    try:
        rdb_crud.insert_books(db, title)
    except InternalError as e:
        db.rollback()
        books = rdb_crud.get_books(db)
        timestamp = datetime.now(const.JST).isoformat()[0:23]  # 日本時間のミリ秒3桁までの文字列
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "aws_az": const.AWS_AZ,
                "private_ip": const.PRIVATE_IP,
                "error_msg": f"データの更新に失敗しました ☠️ 原因: {e.orig}",
                "timestamp": timestamp,
                "books": books,
            }
        )
    except Exception as e:
        db.rollback()
        books = rdb_crud.get_books(db)
        timestamp = datetime.now(const.JST).isoformat()[0:23]  # 日本時間のミリ秒3桁までの文字列
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "aws_az": const.AWS_AZ,
                "private_ip": const.PRIVATE_IP,
                "error_msg": f"データの更新に失敗しました ☠️ 原因: {e}",
                "timestamp": timestamp,
                "books": books,
            }
        )
    # INSERTが成功したらトップへリダイレクト、status_codeなしだとpostリクエストのループになる
    return RedirectResponse("/", status_code=302)


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
