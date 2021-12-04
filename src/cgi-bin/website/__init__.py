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
    """This function binds the different modules used into a package, so if it is called it runs through all the initializations and imports
    
    Returns:
        Flask: our application
    
    Test 1: call the function and test if all initializations and imports work correct
    Test 2: test if the database is created successfully
    """
    
    app = Flask(__name__) # initializing flask

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

    #This will bind the Flask-Login to the server
    login_manager = LoginManager() 
    login_manager.init_app(app)
    login_manager.login_view = 'auth/login.html' #gives the standard url when logging in
    
    @login_manager.user_loader
    def load_user(id):
        """This callback is used to reload the user object from the user ID stored in the session.

        Args:
            id (sqlalchemy.orm.attributes.InstrumentedAttribute): is used as primary key in the UserList table

        Returns:
            UserList: corresponding user object
            
        Test 1: test if the right user is given back for a certain id
        Test 2: test if the right data type is returned
        """
        return  UserList.query.get(int(id))



    return app