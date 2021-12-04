from flask import Blueprint, render_template, flash
from website.user import User

auth = Blueprint('auth', __name__)

@auth.route('/sign-up')
def register():
    return render_template('auth/sign-up.html')
    
@auth.route('/sign-in')
def login():
    return render_template('auth/sign-in.html')

@auth.route('/registerd-successfull/')
def registerdSuccessfull():

    flash('User was registerd successfull - You are now able to log in with your credentials', 'alert-success')
    return render_template('auth/sign-in.html', flashArea='TEST')

@auth.route('/logout')
def logout():
    user = User()
    result = user.logout()
    flash('Log out was successfull!')
    return render_template('auth/sign-up.html')