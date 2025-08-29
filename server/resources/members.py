# server/resources/members.py
from flask import session
from flask_restful import Resource
from models import db, Article

class MemberOnlyIndex(Resource):
    def get(self):
        # require logged-in user
        if not session.get('user_id'):
            return {"error": "Unauthorized"}, 401

        articles = Article.query.filter_by(is_member_only=True).all()
        return [a.to_dict() for a in articles], 200


class MemberOnlyArticle(Resource):
    def get(self, id):
        # require logged-in user
        if not session.get('user_id'):
            return {"error": "Unauthorized"}, 401

        # use session.get to avoid Query.get deprecation (if available)
        article = db.session.get(Article, id)
        if not article or not article.is_member_only:
            return {"error": "Not found"}, 404

        return article.to_dict(), 200
