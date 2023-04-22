import rdb_models as models
from rdb import engine


if __name__ == '__main__':
    models.Books.__table__.drop(engine)
