from flask import jsonify
from werkzeug.exceptions import HTTPException

from .auth import auth
from .movies import movies


def init_routes(app):
    app.register_blueprint(auth)
    app.register_blueprint(movies)

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify(error='Such path is not found.')

    @app.errorhandler(Exception)
    def handle_error(e):
        app.logger.error(e)
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return jsonify(error='We have technical difficulties.'), code
