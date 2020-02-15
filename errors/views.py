from flask import render_template, redirect
from app import app, login_manager


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error=404, discription="Файл не найден или находится в разработке")


@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', error=500, discription="Проблемы с сервером или ведутся санитарные работы")


@login_manager.unauthorized_handler
def authorize():
    return redirect('users/login')
