from news.views import index, news_info
from flask import Blueprint

bp = Blueprint("news", __name__, url_prefix="/")
bp.add_url_rule("", view_func=index)
bp.add_url_rule("news/<int:news_id>", view_func=news_info)
