from flask import Blueprint, render_template, flash
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

    flash('Ihr Profil wurde erfolgreich registriert - Sie können sich jetzt mit Ihren Zugangsdaten anmelden', 'alert-success')
    return render_template('auth/sign-in.html', flashArea='TEST')

@auth.route('/logout')
def auth_logout():
    user = User()
    result = user.logout()
    flash('Sie haben sich erfolgreich ausgelogt', 'alert-success')
    return render_template('auth/sign-in.html')