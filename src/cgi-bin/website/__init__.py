"""
    author: Felix Kapfer
    date: 12.11.2021
    license: private
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager, login_manager
from datetime import date

db = SQLAlchemy()
ma = Marshmallow()



def createApp():
    app = Flask(__name__)

    #app.config['SECRET KEY'] = 'gheckoprojectname2021 - Group: Programmieren Next Level'
    app.secret_key = 'gheckoprojectname2021 - Group: Programmieren Next Level'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    
    db.init_app(app)
    ma.init_app(app)

    from .views import views
    from .auth import auth
    from .api import api
    from . import httpErrorHandler

    from .model import UserList, ProjectList
    app.app_context().push()
    db.create_all()

    app.register_error_handler(400, httpErrorHandler.bad_request)
    app.register_error_handler(401, httpErrorHandler.unauthorized)
    app.register_error_handler(403, httpErrorHandler.forbidden)
    app.register_error_handler(404, httpErrorHandler.page_not_found)
    app.register_error_handler(405, httpErrorHandler.method_not_allowed)
    app.register_error_handler(408, httpErrorHandler.request_timeout)
    app.register_error_handler(500, httpErrorHandler.internal_server_error)
    app.register_error_handler(501, httpErrorHandler.not_implemented)
    app.register_error_handler(502, httpErrorHandler.bad_gateway)
    app.register_error_handler(503, httpErrorHandler.service_unavailable)
    app.register_error_handler(504, httpErrorHandler.gateway_timeout)
    app.register_error_handler(505, httpErrorHandler.http_version_not_supported)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')
    app.register_blueprint(api, url_prefix='/api/')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth/login.html'
    
    @login_manager.user_loader
    def load_user(id):
        return UserList.query.get(int(id))



    return app