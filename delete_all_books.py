from sqlalchemy.orm import Session

import const
import rdb_crud
import rdb_models as models
from rdb import SessionLocal, engine


if __name__ == '__main__':
    with Session(engine) as session:
        session.query(models.Books).delete()
        session.commit()
