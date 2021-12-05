from flask import Blueprint, render_template, flash
from flask.helpers import url_for
from werkzeug.utils import redirect
from website.user import User

auth = Blueprint('auth', __name__)

@auth.route('/sign-up')
def auth_register():
    """This functions renders the sign up page when the /sign-up URL is called 

    Returns:
        html: the sign up page
        
    Test: calling the url and see if it renders the right template
    """
    
    return render_template('auth/sign-up.html')
    
@auth.route('/sign-in')
def auth_login():
    """This functions renders the sign in page when the /sign-in URL is called 

    Returns:
        html: the sign in page
        
    Test: calling the url and see if it renders the right template
    """
    return render_template('auth/sign-in.html')

@auth.route('/registerd-successfull/')
def auth_registerdSuccessfull():
    """This functions renders the sign in page when the /registerd-successfull URL is called

    Returns:
        html: the sign in page
        
    Test: calling the url and see if it renders the right template
    """

    flash('Ihr Profil wurde erfolgreich registriert - Sie können sich jetzt mit Ihren Zugangsdaten anmelden', 'alert-success')
    return render_template('auth/sign-in.html', flashArea='TEST')

@auth.route('/logout')
def auth_logout():
    """This functions renders the login page when the /logout URL is called and logs the user out

    Returns:
        html: login page
        
    Test 1: calling the url and see if it renders the right template
    Test 2: test if the user is logged out succesfully
    """
    user = User()
    result = user.logout()
    flash('Sie haben sich erfolgreich ausgelogt', 'alert-success')
    return redirect(url_for('auth.auth_login'))
