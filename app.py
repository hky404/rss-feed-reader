from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db_uri = 'postgresql://feed_user:feed_platform20am@localhost/rssfeedreader'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri