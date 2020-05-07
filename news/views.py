from flask import render_template
from news.models import News
from base64 import b64encode


def index():
    news = News.query.order_by(News.date.desc())
    return render_template('news/index.html', news=news, b64encode=b64encode)


def news_info(news_id):
    return render_template("news/news.html", news=News.get_by(id=news_id))
