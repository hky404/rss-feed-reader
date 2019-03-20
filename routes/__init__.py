from flask import abort, redirect, request, render_template
from app import app
from db import db
from models.article import Article
from models.feed_source import FeedSource
import feed


@app.route('/', methods=['GET'])
def index_get():
    query = Article.query
    query = query.filter(Article.unread == True)
    orderby = request.args.get('orderby', 'added')
    if orderby == 'added':
        query = query.order_by(Article.feed_source_sid, Article.created_at.desc())
    elif orderby == 'published':
        query = query.order_by(Article.feed_source_sid, Article.source_updated_at.desc())
    elif orderby == 'title':
        query = query.order_by(Article.feed_source_sid, Article.title)

    articles = query.all()
    return render_template('index.html', articles=articles)


@app.route('/read/<int:sid>', methods=['GET'])
def read_article_get(sid):
    article = Article.query.get(sid)
    article.unread = False
    db.session.commit()
    return redirect(article.link)


@app.route('/sources', methods=['GET'])
def sources_get():
    query = FeedSource.query
    query = query.order_by(FeedSource.title.desc())
    feed_sources = query.all()
    return render_template('sources.html', feed_sources=feed_sources)


@app.route('/sources', methods=['POST'])
def sources_post():
    feed_url = request.form['feed']
    parsed = feed.parse(feed_url)
    feed_source = feed.get_source(parsed)
    source = FeedSource.insert_from_feed(feed_url, feed_source)
    feed_articles = feed.get_articles(parsed)
    Article.insert_from_feed(source.sid, feed_articles)
    return redirect('/sources')
