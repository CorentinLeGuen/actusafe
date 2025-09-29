import html
import os
import unicodedata
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

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


def create_get_category(name: str) -> Category:
    existing = session.query(Category).filter_by(name=name).first()
    if existing:
        return existing

    try:
        new_cat = Category(name=name)
        session.add(new_cat)
        session.commit()
        session.refresh(new_cat)
        return new_cat
    except Exception:
        session.rollback()
        again = session.query(Category).filter_by(name=name).first()
        if again:
            return again
        raise


def create_get_source(name: str) -> Source:
    existing = session.query(Source).filter_by(name=name).first()
    if existing:
        return existing

    try:
        new_source = Source(name=name)
        session.add(new_source)
        session.commit()
        session.refresh(new_source)
        return new_source
    except Exception:
        session.rollback()
        again = session.query(Source).filter_by(name=name).first()
        if again:
            return again
        raise


def add_article(article: Article):
    existing = session.query(Article).filter_by(article_name=article.article_name).first()
    if existing:
        # update existing article
        existing.article_name = article.article_name
        existing.subtitle = article.subtitle
        existing.lead_text = article.lead_text
        existing.thumbnail = article.thumbnail
        existing.publish_date = article.publish_date
        existing.updated_at = article.updated_at
        existing.origin_url = article.origin_url
        existing.categories = article.categories
        session.commit()
        return
    try:
        session.add(article)
        session.commit()
        return
    except Exception:
        session.rollback()
        return


def cleanup_text(text: str) -> str:
    if text is None:
        return ""
    decoded_html = html.unescape(text)
    normalized = unicodedata.normalize('NFKC', decoded_html)
    normalized = normalized.replace('\u00A0', ' ')
    return ''.join(c for c in normalized if unicodedata.category(c)[0] != 'C')
