from flask import Blueprint, jsonify, request
from ..models import NewsPost


news_bp = Blueprint("news_bp", __name__, url_prefix="/api")


@news_bp.route("/news", methods=["GET"])  #Route for showing news in AboutUs page
def get_news():
    lang = request.args.get('lang', 'en')
    posts = NewsPost.query.order_by(NewsPost.created_at.desc()).all()
    return jsonify([post.to_dict(lang=lang) for post in posts]), 200
