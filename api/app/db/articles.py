import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, joinedload

Base = declarative_base()
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

article_category = Table(
    'article_category',
    Base.metadata,
    Column('article_id', ForeignKey('articles.id'), primary_key=True),
    Column('category_id', ForeignKey('category.id'), primary_key=True),
)


class Source(Base):
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    articles = relationship('Article', back_populates='source', lazy='dynamic')


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)

    articles = relationship('Article', secondary=article_category, back_populates="categories")


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    article_name = Column(String, index=True)
    subtitle = Column(String)
    lead_text = Column(String)
    thumbnail = Column(String)
    publish_date = Column(String)
    updated_at = Column(String)
    origin_url = Column(String)
    scrapped_at = Column(DateTime(timezone=True), default=func.now())

    categories = relationship(
        "Category",
        secondary=article_category,
        back_populates="articles",
    )

    source_id = Column(Integer, ForeignKey('sources.id'), nullable=False, index=True)
    source = relationship(
        "Source",
        back_populates="articles",
    )


Base.metadata.create_all(bind=engine)


def get_stored_articles():
    return (
        session.query(Article)
        .options(
            joinedload(Article.source),
            joinedload(Article.categories),
        )
        .all()
    )
