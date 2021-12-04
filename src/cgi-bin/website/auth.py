from flask import Blueprint, render_template, flash
from website.user import User

auth = Blueprint('auth', __name__)

@auth.route('/sign-up')
def register():
    """This functions renders the sign up page when the /sign-up URL is called 

    Returns:
        html: the sign up page
        
    Test: calling the url and see if it renders the right template
    """
    return render_template('auth/sign-up.html')
    
@auth.route('/sign-in')
def login():
    """This functions renders the sign in page when the /sign-in URL is called 

    Returns:
        html: the sign in page
        
    Test: calling the url and see if it renders the right template
    """
    return render_template('auth/sign-in.html')

@auth.route('/registerd-successfull/')
def registerdSuccessfull():
    """This functions renders the registerd successfull page when the /registerd-successfull URL is called

    Returns:
        html: the registerd successfull page
        
    Test: calling the url and see if it renders the right template
    """

    flash('User was registerd successfull - You are now able to log in with your credentials', 'alert-success')
    return render_template('auth/sign-in.html', flashArea='TEST')

@auth.route('/logout')
def logout():
    """This functions renders the sign up page when the /logout URL is called and logs the user out

    Returns:
        html: the sign up page
        
    Test 1: calling the url and see if it renders the right template
    Test 2: test if the user is logged out succesfully
    """
    user = User()
    result = user.logout()
    flash('Log out was successfull!')
    return render_template('auth/sign-up.html')