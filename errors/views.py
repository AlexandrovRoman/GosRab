from flask import render_template, redirect, url_for
from app import app


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', error=404)


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=500)


@app.errorhandler(401)
def user_not_auth(error):
    return redirect(url_for('users/login/'))
