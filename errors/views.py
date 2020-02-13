from flask import render_template
from app import app
import logging
from logging.handlers import RotatingFileHandler

file_handler = RotatingFileHandler('logs/server.log', maxBytes=1024 * 1024, encoding='utf-8', mode='w')
file_handler.setFormatter(logging.Formatter('%(message)s\nin %(pathname)s:%(lineno)d\n'
                                            '-----------------------------------------------------------------------'))
app.logger.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)


@app.errorhandler(404)
def not_found_error(error):
    app.logger.error(error)
    return render_template('404.html')


@app.errorhandler(500)
def server_error(error):
    app.logger.error(error)
    return render_template('500.html')
