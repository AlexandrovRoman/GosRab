from flask import render_template
from news.models import HotNews, News


def index():
    hot_news = HotNews.all()
    news = News.all()
    return render_template('news/news.html', hot_news=hot_news, news=news)
