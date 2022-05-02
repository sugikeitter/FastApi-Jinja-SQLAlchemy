from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from rdb import Base


class Books(Base):
    """
    CREATE TABLE books (
        book_id VARCHAR ( 50 ) PRIMARY KEY,
        title VARCHAR ( 100 ) NOT NULL,
        created_on TIMESTAMP NOT NULL,
        updated_on TIMESTAMP NOT NULL
        );
    """
    __tablename__ = "books"

    book_id = Column(String, primary_key=True, index=True)
    title = Column(String)
    created_on = Column(String)
    updated_on = Column(Integer)
