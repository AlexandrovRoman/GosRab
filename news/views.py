from flask import render_template
from news.models import HotNews, News


def index():
    hot_news = HotNews.get_news()
    news = News.get_courses()
    return render_template('news/news.html', hot_news=hot_news, news=news)
