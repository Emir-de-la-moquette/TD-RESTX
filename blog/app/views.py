from flask_restx import Resource, Namespace, abort
from .api_models import *
from .models import *

# Création du namespace, racine de tous les endpoints
ns = Namespace("api")

# Définition d’une route
@ns.route("/hello")  # Pas d'espace après les guillemets
class Hello(Resource):
    def get(self):
        return {"hello": "restx"}

@ns.route("/articles")
class ArticleCollection(Resource):
    @ns.marshal_list_with(article_model)
    def get(self):
        return get_all_articles()
    
    @ns.expect(article_model)
    @ns.marshal_with(article_model)
    def post (self) :
        article = create_article (title = ns.payload["title"], content = ns.payload["content"])
        return {article} ,201
    
@ns.route( "/articles/<int:id>" )
@ns.response(404 , 'Article not found')
class ArticleItem (Resource) :
    @ns.marshal_with( article_model )
    def get (self, id) :
        article = get_article(id)
        if article is None :
            abort (404 , "Article not found" )
            return article
        
    @ns.expect(article_input_model)
    @ns.marshal_with(article_model)
    def put (self, id) :
        title = ns.payload ["title"]
        content = ns.payload ["content"]
        article = modify_article(id, title, content)
        if article is None :
            abort (404 , "Article not found" )
            return article , 200



    
@ns.route("/comments")
class CommentsCollection(Resource):
    @ns.marshal_list_with(comment_model)
    def get(self):
        return get_all_comments()
    
@ns.route( "/comments/<int:id>" )
@ns.response(404 , 'Comment not found')
class CommentItem (Resource) :
    @ns.marshal_with( comment_model )
    def get (self, id) :
        comment = get_comment(id)
        if comment is None :
            abort (404 , "Comment not found" )
            return comment