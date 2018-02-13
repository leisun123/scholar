# coding: utf-8
from sqlalchemy import ARRAY, BigInteger, Column, DateTime, Float, Index, Integer, Numeric, String, Table, Text, INTEGER
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    title = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer)
    citations_count = db.Column(db.Integer)
    link = db.Column(db.Text)
    bibtex = db.Column(db.Text)
    resource_type = db.Column(db.Text)
    resource_link = db.Column(db.Text)
    summary = db.Column(db.Text)
    google_id = db.Column(db.Text, unique=True)
    citations_link = db.Column(db.Text)
    is_downloaded = db.Column(db.Integer, server_default=db.FetchedValue())
    journal_temp_info = db.Column(db.String(200))
    pdf_temp_url = db.Column(db.String(200))
    site = db.Column(db.Text)
    keywords = db.Column(db.Text)
    is_keywords_available = db.Column(db.Text)
    authors = db.Column(db.Text, index=True)
    volume_db_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    id_by_journal = db.Column(db.Text)
    journal_id = db.Column(db.BigInteger)
    create_time = db.Column(db.DateTime)


class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    article_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    


t_organization_scores = db.Table(
    'organization_scores',
    db.Column('id', db.Integer),
    db.Column('sum', db.Numeric)
)


class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=False)
    scholars_count = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    country = db.Column(db.Text)
    province = db.Column(db.Text)
    city = db.Column(db.Text)
    latitude = db.Column(db.Float(53))
    longitude = db.Column(db.Float(53))
    geo = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    acronym = db.Column(db.Text)
    link = db.Column(db.Text)
    google_place_id = db.Column(db.Text)
    google_place_search_response = db.Column(db.Text)
    google_place_details_response = db.Column(db.Text)
    wikipedia_page = db.Column(db.Text)
    description = db.Column(db.Text)


class Pdf(db.Model):
    __tablename__ = 'pdf'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    article_id = db.Column(db.BigInteger, nullable=False, unique=True)
    google_id = db.Column(db.Text, nullable=False)
    link = db.Column(db.Text, nullable=False)
    size = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    state = db.Column(db.Text)
    retry = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())


t_schema_migrations = db.Table(
    'schema_migrations',
    db.Column('version', db.String, nullable=False, unique=True)
)


class ScholarArticle(db.Model):
    __tablename__ = 'scholar_articles'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    scholar_id = db.Column(db.Integer, nullable=False)
    article_id = db.Column(db.Integer, nullable=False)


t_scholar_articles_count = db.Table(
    'scholar_articles_count',
    db.Column('scholar_id', db.Integer),
    db.Column('count', db.BigInteger)
)


t_scholar_articles_counts = db.Table(
    'scholar_articles_counts',
    db.Column('scholar_id', db.Integer),
    db.Column('count', db.BigInteger)
)


t_scholar_citations_count = db.Table(
    'scholar_citations_count',
    db.Column('scholar_id', db.Integer),
    db.Column('sum', db.BigInteger)
)


t_scholar_citations_counts = db.Table(
    'scholar_citations_counts',
    db.Column('scholar_id', db.Integer),
    db.Column('sum', db.BigInteger)
)


t_scholar_cooperations = db.Table(
    'scholar_cooperations',
    db.Column('article_id', db.Integer),
    db.Column('scholar_ids', db.ARRAY(INTEGER())),
    db.Column('citations_count', db.Integer)
)


class ScholarCooperator(db.Model):
    __tablename__ = 'scholar_cooperators'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    scholar_id = db.Column(db.Integer, nullable=False)
    cooperator_id = db.Column(db.Integer, nullable=False)


t_scholar_cooperators_count = db.Table(
    'scholar_cooperators_count',
    db.Column('scholar_id', db.Integer),
    db.Column('count', db.BigInteger)
)


t_scholar_cooperators_counts = db.Table(
    'scholar_cooperators_counts',
    db.Column('scholar_id', db.Integer),
    db.Column('count', db.BigInteger)
)


class Scholar(db.Model):
    __tablename__ = 'scholars'

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.Text)
    job_title = db.Column(db.Text)
    address = db.Column(db.Text)
    email = db.Column(db.Text)
    phone = db.Column(db.Text)
    website = db.Column(db.Text)
    vita = db.Column(db.Text)
    created_at = db.Column(db.DateTime(True))
    updated_at = db.Column(db.DateTime(True))
    first_name = db.Column(db.Text)
    middle_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    state = db.Column(db.String)
    latitude = db.Column(db.Float(53))
    longitude = db.Column(db.Float(53))
    country = db.Column(db.Text)
    province = db.Column(db.Text)
    city = db.Column(db.Text)
    organization_id = db.Column(db.Integer)
    is_added = db.Column(db.Integer)


t_scholars_with_citation_counts = db.Table(
    'scholars_with_citation_counts',
    db.Column('id', db.BigInteger),
    db.Column('name', db.Text),
    db.Column('job_title', db.Text),
    db.Column('address', db.Text),
    db.Column('email', db.Text),
    db.Column('phone', db.Text),
    db.Column('website', db.Text),
    db.Column('vita', db.Text),
    db.Column('created_at', db.DateTime(True)),
    db.Column('updated_at', db.DateTime(True)),
    db.Column('first_name', db.Text),
    db.Column('middle_name', db.Text),
    db.Column('last_name', db.Text),
    db.Column('state', db.String),
    db.Column('latitude', db.Float(53)),
    db.Column('longitude', db.Float(53)),
    db.Column('country', db.Text),
    db.Column('province', db.Text),
    db.Column('city', db.Text),
    db.Column('organization_id', db.Integer),
    db.Column('scholar_id', db.Integer),
    db.Column('sum', db.BigInteger)
)


t_scholars_with_cooperator_counts = db.Table(
    'scholars_with_cooperator_counts',
    db.Column('id', db.BigInteger),
    db.Column('name', db.Text),
    db.Column('job_title', db.Text),
    db.Column('address', db.Text),
    db.Column('email', db.Text),
    db.Column('phone', db.Text),
    db.Column('website', db.Text),
    db.Column('vita', db.Text),
    db.Column('created_at', db.DateTime(True)),
    db.Column('updated_at', db.DateTime(True)),
    db.Column('first_name', db.Text),
    db.Column('middle_name', db.Text),
    db.Column('last_name', db.Text),
    db.Column('state', db.String),
    db.Column('latitude', db.Float(53)),
    db.Column('longitude', db.Float(53)),
    db.Column('country', db.Text),
    db.Column('province', db.Text),
    db.Column('city', db.Text),
    db.Column('organization_id', db.Integer),
    db.Column('scholar_id', db.Integer),
    db.Column('count', db.BigInteger)
)


class SubjectArticle(db.Model):
    __tablename__ = 'subject_articles'
    __table_args__ = (
        db.Index('index_subject_articles_on_subject_id_and_article_id', 'subject_id', 'article_id'),
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    subject_id = db.Column(db.Integer, nullable=False)
    article_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)


