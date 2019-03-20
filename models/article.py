from db import db
import datetime
from sqlalchemy.dialects.postgresql import insert


class Article(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    source_system_id = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    link = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    source_updated_at = db.Column(db.DateTime)
    unread = db.Column(db.Boolean, default=True, nullable=False)
    feed_source_sid = db.Column(db.Integer, db.ForeignKey('feed_source.sid'), nullable=False)
    feed_source = db.relationship('FeedSource', backref=db.backref('article', lazy=True))
    __table_args__ = (
        db.UniqueConstraint('feed_source_sid', 'source_system_id', name='uc_feed_source_id'),
    )

    @classmethod
    def insert_from_feed(cls, feed_source_sid, feed_articles):
        articles = []
        for article in feed_articles:
            articles.append({
                'title': article['title'],
                'body': article['summary'],
                'link': article['link'],
                'source_system_id': article['id'],
                'source_updated_at': article['source_updated_at'],
                'feed_source_sid': feed_source_sid
            })

        insert_stmt = insert(Article).values(articles).on_conflict_do_nothing(constraint='uc_feed_source_id')
        db.engine.execute(insert_stmt)
