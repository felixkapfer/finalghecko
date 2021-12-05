from flask import Blueprint, render_template, flash
from flask.helpers import url_for
from werkzeug.utils import redirect
from website.user import User

auth = Blueprint('auth', __name__)

@auth.route('/sign-up')
def auth_register():
    return render_template('auth/sign-up.html')
    
@auth.route('/sign-in')
def auth_login():
    return render_template('auth/sign-in.html')

@auth.route('/registerd-successfull/')
def auth_registerdSuccessfull():

    flash('User was registerd successfull - You are now able to log in with your credentials', 'alert-success')
    return render_template('auth/sign-in.html', flashArea='TEST')

@auth.route('/logout')
def auth_logout():
    user = User()
    result = user.logout()
    flash('Log out was successfull!')
    # return render_template('auth/sign-in.html')
    return redirect(url_for('auth.auth_login'))