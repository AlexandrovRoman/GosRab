from flask import render_template
from news.models import News, Courses


def index():
    news = News.get_news()
    courses = Courses.get_courses()
    return render_template('news.html', news=news, courses=courses)
