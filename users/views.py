from flask import render_template


def hello():
    return render_template('test.html')


def start():
    return 'start'
