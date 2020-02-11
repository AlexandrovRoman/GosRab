from flask import render_template, request


def hello():
    print(request.method, 'request')
    return render_template('test.html')


def start():
    return 'start'
