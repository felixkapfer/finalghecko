# Imports for Errorhandling
from sqlalchemy.orm.exc import NoResultFound #"1" errorcode
from sqlalchemy.orm.exc import MultipleResultsFound #6
from sqlalchemy.exc import IntegrityError #2
from sqlalchemy.exc import CompileError #3
from sqlalchemy.exc import DBAPIError #4
from sqlalchemy.exc import InternalError #5
from sqlalchemy.exc import NoReferencedTableError #7
from sqlalchemy.exc import ObjectNotExecutableError #8
from sqlalchemy.exc import SQLAlchemyError #10

# Imports for Falsk Login
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Other Imports
from . import db
from .model import UserList
from .modelMetaData import UserList




# User Class
class User:
    """The class User is used to register, login and logout a user. It takes variables from the API and processes them in the functions.
       Therefore it creates an user if you register, logs an user in if the args are valid and logs an user out if he/she is logged in. 
       It uses multiple functions from the flask_login module.
    """

    def __init__(self, logged_in = None, result = None, error = None): 
    # def __init__(self): 
        """Constructor that initializes the variables

        Args:
            logged_in (boolean): Inherits the login status of an user if he/she is logged in or not. Defaults to None.
            result (user): user data (e.g. firstname, lastname, email, etc.). Defaults to None.
            error (int): Stands for the type of error. Defaults to None.
        """
        
        self.logged_in = None 
        self.error     = None
        self.result    = None
    


    
    def __user__setLoggedIn(self, logged_in):
        """Setter function for variable logged_in

        Args:
            logged_in (boolean): login status of an user (true = user is logged in, false = user is not logged in)
        """
        
        self.logged_in = logged_in
    



    def __user_getLoggedIn(self):
        """Getter function for variable logged_in

        Returns:
            [boolean]: login status of an user (true = user is logged in, false = user is not logged in)
        """
        
        return self.logged_in
    



    def __user__setResult(self, result):
        """Setter function for variable result 

        Args:
            result (user): user data
        """
        
        self.result = result
    



    def __user_getResult(self):
        """Getter function for the variable result

        Returns:
            [user]: user data
        """
        
        return self.result
    



    def __user_setError(self, error):
        """Setter function for the variable error

        Args:
            error (int): Stands for the type of error.
        """
        
        self.error = error
    



    def __user_getError(self):
        """Getter function for the variable error

        Returns:
            [int]: type of error
        """
        
        return self.error
    
    LoggedIn = property(__user_getLoggedIn)
    Error    = property(__user_getError)
    Result   = property(__user_getResult)




    # -------------------------------------------------------------------------------------------------------------------------
    # Define backend function that interact with the Database to register a User
    # -------------------------------------------------------------------------------------------------------------------------

    def user_register(self, args):
        """Registration of an potential user
            *takes the given args and checks if they are valid 
            *creates an user in the database with the given args
            *logs in the user 
            *sets logged_in to true

        Args:
            args (~werkzeug.datastructures.ImmutableMultiDict): Data from the API, which the user entered (posted)
            
        Test:
            * Test 1: Trying to register with invalid parameters
            * Test 2: Test if a new user was added

        Returns:
            [boolean]: result of the function (if succesful -> true, else -> false)
        """
              
        firstname = args['firstname']
        lastname  = args['lastname']
        email     = args['email']
        pwd       = args['pwd']

        # tries to create a new user in the database with the given args
        try:            
            count_user = UserList.query.filter_by(email=email).count()
            if count_user == 0 :
                pwd_hashed = generate_password_hash(pwd, method='sha256')
                new_user   = UserList(firstname=firstname, lastname=lastname, email=email, pwd=pwd_hashed)
                db.session.add(new_user)
                db.session.commit()
    
            elif count_user != 0:
                raise IntegrityError('', '', '')

        except NoResultFound:
            db.session.rollback
            self.__user_setError("1")
            return False
        except IntegrityError:
            db.session.rollback
            self.__user_setError("2")
            return False
        except CompileError:
            db.session.rollback
            self.__user_setError("3")
            return False
        except DBAPIError:
            db.session.rollback
            self.__user_setError("4")
            return False
        except InternalError:
            db.session.rollback
            self.__user_setError("5")
            return False
        except MultipleResultsFound:
            db.session.rollback
            self.__user_setError("6")
            return False
        except NoReferencedTableError:
            db.session.rollback
            self.__user_setError("7")
            return False
        except ObjectNotExecutableError:
            db.session.rollback
            self.__user_setError("8")
            return False
        except SQLAlchemyError:
            db.session.rollback
            self.__user_setError("9")
            return False
        else:
            self.__user_setError("")
            return True


    # -------------------------------------------------------------------------------------------------------------------------
    # Define backend function that interact with the Database to log User in
    # -------------------------------------------------------------------------------------------------------------------------
    def user_login(self, args):
        """Login of an user
            *extends from the flask
            *takes the given args and checks if they belong together, if the passwort for the given email is correct
            *logs in the user
            *sets logged_in to true

        Args:
            args (~werkzeug.datastructures.ImmutableMultiDict): Data from the API, which the user entered (posted)

            
        Test:
            * Test 1: Trying to login with invalid parameters -> try to log in with an email that was never registered or try to log in with a wrong password
            * Test 2: Test if user is logged in -> after logging in check if the users data is saved in the variable current_user

        Returns:
            [boolean]: result of the function (if succesful -> true, else -> false)
        """
        
        email = args['email']
        pwd   = args['pwd']

        try:
            count_user = UserList.query.filter_by(email=email).count()                      # Checks if the user exists by searching for the email
            if count_user == 0:                                                             # If no user was found by searching for the email it will raise a NoResultFound Error                
                raise NoResultFound

            elif count_user != 1:                                                           # If there were found more than one users it will raise an Integrity Error 
                raise IntegrityError('', '', '')
            
            elif count_user == 1:                                                           # If there was found exaclty one user, this user will be passed to the variable user 
                user = UserList.query.filter_by(email=email).first()   
            
            else:                                                                           # For all other cases it will raise an InternalError
                raise InternalError


        except NoResultFound:
            db.session.rollback
            self.__user_setError("1")
            return False
        except IntegrityError:
            self.__user_setError("2")
            db.session.rollback
            return False
        except CompileError:
            self.__user_setError("3")
            db.session.rollback
            return False
        except DBAPIError:
            self.__user_setError("4")
            db.session.rollback
            return False
        except InternalError:
            self.__user_setError("5")
            db.session.rollback
            return False
        except MultipleResultsFound:
            self.__user_setError("6")
            db.session.rollback
            return False
        except NoReferencedTableError:
            self.__user_setError("7")
            db.session.rollback
            return False
        except ObjectNotExecutableError:
            self.__user_setError("8")
            db.session.rollback
            return False
        except SQLAlchemyError:
            self.__user_setError("9")
            db.session.rollback
            return False
        else:
            if check_password_hash(user.pwd, pwd):                                  # checks if the password is matching the password in the database for that user
                login_user(user, remember=False)                                    # flask-login method to log user in
                self.__user__setLoggedIn(True)
                return True
            else:                                                                   # if user typed in a wrong password, it will return false
                self.__user_setError('10')
                return False



    # -------------------------------------------------------------------------------------------------------------------------
    # Define backend function that interact with the Database to log User in
    # -------------------------------------------------------------------------------------------------------------------------
    @login_required
    def logout(self):
        """Logout of an user
            *checks if an user is logged in
            *if the user is logged in it logs the user out
            *then it sets logged_in to false
            
        Test:
            * Test 1: Test if user is really logged out -> check the variable current_user if it still contains the users data or check if the logged_in variable == False
            * Test 2: Try to logout if no user is currently logged in -> logout without being logged in 

        Returns:
            [boolean]: result of the function (if succesful -> true, else -> false)
        """

        logout_user()
        if current_user.is_anonymous == True:           # Checks if the user is actually logged out
            self.__user__setLoggedIn(False)
            return True
        else:
            self.__user_setError('11')
            return False