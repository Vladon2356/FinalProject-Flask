import contextlib

from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint


from config import BaseConfig
from api import views as api_views



def clear_database():
    from cinema.database.db import db, base, session

    with contextlib.closing(db.connect()) as con:
        trans = con.begin()
        con.execute(
            "TRUNCATE {} RESTART IDENTITY;".format(
                ",".join(table.name for table in reversed(base.metadata.sorted_tables))
            )
        )
        trans.commit()


def setup_database(app):
    from cinema.database.db import db, base, session

    with app.app_context():

        @app.before_first_request
        def create_tables():
            base.metadata.create_all(db)

def setup_swagger(app):
    SWAGGER_URL = ''
    API_URL = 'static/swagger.yaml'
    swagger_bp = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'Cinema'
        }
    )
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)

def setup_jwt(app):
    jwt = JWTManager(app)

    from cinema.models.revoked_token import RevokedTokenModel

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return RevokedTokenModel.is_jti_blacklisted(jti)


def create_app(config=BaseConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    setup_swagger(app)
    setup_database(app)
    setup_jwt(app)

    from cinema import views

    @app.route('/home/', methods=['GET'])
    def home():
        return render_template('base.html')

    app.register_blueprint(views.users_bp, url_prefix="/users")
    app.register_blueprint(views.movies_bp, url_prefix="/movies")
    app.register_blueprint(views.sessions_bp, url_prefix="/sessions")
    app.register_blueprint(views.tickets_bp, url_prefix="/tickets")
    app.register_blueprint(views.halls_bp, url_prefix="/halls")
    app.register_blueprint(views.auth_bp, url_prefix="/auth")
    app.register_blueprint(api_views.auth_api_bp, url_prefix="/api/auth")
    app.register_blueprint(api_views.users_api_bp, url_prefix="/api/users")
    app.register_blueprint(api_views.movies_api_bp, url_prefix="/api/movies")
    app.register_blueprint(api_views.sessions_api_bp, url_prefix="/api/sessions")

    return app
