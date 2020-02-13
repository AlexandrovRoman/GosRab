from flask import render_template, request


def hello():
    if request.method == 'POST':
        if request.form['username'] == 'ggg' and request.form['password'] == '123':
            return render_template('news.html')

        # return render_template('news.html')
    return render_template('test.html')


def start():
    return 'start'
