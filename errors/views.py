from flask import render_template, redirect, url_for


def not_found_error(error):
    return render_template('errors/error.html', error=404, description="Файл не найден или находится в разработке")


def forbidden(error):
    return render_template('errors/error.html', error=403,
                           description="Ваших прав не достаточно для доступа к данному ресурсу")


def server_error(error):
    return render_template('errors/error.html', error=500,
                           description="Проблемы с сервером или ведутся санитарные работы")


def page_not_implemented(error):
    return render_template('errors/error.html', error=501,
                           description="Данная страница находится в разработке")


def authorize():
    return redirect(url_for('login'))
