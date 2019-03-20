import feedparser


def parse(url):
    return feedparser.parse(url)


def get_source(parsed):
    feed = parsed['feed']
    return {
        'link': feed['link'],
        'title': feed['title'],
        'subtitle': feed['subtitle'],
        'source_updated_at': feed['updated']
    }


def get_articles(parsed):
    articles = []
    feed = parsed['feed']
    entries = parsed['entries']
    for entry in entries:
        articles.append({
            'id': entry['id'],
            'link': entry['link'],
            'title': entry['title'],
            'summary': entry['summary'],
            'source_updated_at': feed['updated']
        })
    return articles
