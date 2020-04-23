from flask import jsonify
from werkzeug.exceptions import HTTPException

from .auth import auth
from .index import index
from .me import me
from .projects import projects


def init_routes(app):
    app.register_blueprint(index, url_prefix='/api')
    app.register_blueprint(auth, url_prefix='/api')
    app.register_blueprint(me, url_prefix='/api')
    app.register_blueprint(projects, url_prefix='/api')

    @app.errorhandler(400)
    def bad_request(e):
        app.logger.error(e)
        return jsonify(error=e.description), 400

    @app.errorhandler(404)
    def page_not_found(e):
        print(e)
        return jsonify(error='Such path is not found.'), 404

    @app.errorhandler(Exception)
    def handle_error(e):
        app.logger.error(e)
        print(e)
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return jsonify(error='We have technical difficulties.'), code
