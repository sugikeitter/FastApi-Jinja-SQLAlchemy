from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

import rdb_models as models

JST = timezone(timedelta(hours=+9), 'JST')


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Books).offset(skip).limit(limit).all()


def insert_books(db: Session, book_id: str, title: str):
    dt_now = datetime.now(tz=JST)
    c = models.Books(
        book_id=book_id,
        title=title,
        created_on=dt_now,
        updated_on=dt_now
    )
    db.add(c)
    db.commit()
