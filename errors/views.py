from flask import render_template, redirect, url_for
from app import app


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error=404, discription="Файл не найден или находится в разработке")


@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', error=500, discription="Проблемы с сервером или ведутся санитарные работы")


@app.errorhandler(401)
def login_error(error):
    return redirect(url_for('login'))
