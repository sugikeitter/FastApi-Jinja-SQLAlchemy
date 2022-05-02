from datetime import datetime, timedelta, timezone

from sqlalchemy import desc
from sqlalchemy.orm import Session

import rdb_models as models

JST = timezone(timedelta(hours=+9), 'JST')


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Books)\
        .order_by(desc(models.Books.book_id))\
        .offset(skip)\
        .limit(limit)\
        .all()


def insert_books(db: Session, title: str):
    dt_now = datetime.now(tz=JST)
    c = models.Books(
        title=title,
        created_on=dt_now,
        updated_on=dt_now
    )
    db.add(c)
    db.commit()
