from flask import Blueprint, request, jsonify, json, render_template, abort
from .generalErrorHandler import FormError, DbError
from .validationHandler import Validation
from .user import User
from .task import Task
from .project import Project


api   = Blueprint('api', __name__)



# --------------------------------------------------------------------------------------
# API Interface to create a new user
# --------------------------------------------------------------------------------------
@api.route('/create-user' , methods=['POST'])
def api_createUser():
    """
    This method is used to validate that all necessary data needed to create an user account are provided by the user. All input fields will be validated that it only contains the right data.
    This method will also call the user_createUser function to connect to the database and write the data into the user table
    This method will be executed when the URL extension /create-user is triggered.
    The form data will be validated for:
    * Firstname
        * isEmpty  : will add an Error to the JSON object if no firstname is provided
        * isAlpha  : will add an Error to the JSON object if firstname contains not only alphabetic letters
        * minLength: will add an Error to the JSON object if firstname has less than two letters
    
    * Lastname
        * isEmpty  : will add an Error to the JSON object if no lastname is provided
        * isAlpha  : will add an Error to the JSON object if lastname contains not only alphabetic letters
        * minLength: will add an Error to the JSON object if lastname has less than two letters

    * E-Mail Address
            * isEmpty: will add an Error to the JSON object if no email address is provided
            * isEmail: will add an Error to the JSON object if email has no valid email format

    * Password
            * isEmpty                  : will add an Error to the JSON object if no password is provided
            * minLength                : will add an Error to the JSON object if password has less than 8 letters
            * upperChars               : will add an Error to the JSON object if password has less than one upper character
            * lowerChars               : will add an Error to the JSON object if password has less than one lower character
            * containsDigit            : will add an Error to the JSON object if password has less than one digit
            * containsSpecialChar      : will add an Error to the JSON object if password has less than one special character
            * followPasswordRegulations: will add an Error to the JSON object if password has does not follow the password regulations

    * Confirm Password
            * isEmpty: will add an Error to the JSON object if no password is provided to confirm the first one
            * noMath : will add an Error to the JSON object if password and confirm password do not match

    Returns:
        JSON object: This method returns a JSON object that contains information about occured errors if registration was not successfull as well as some metadata where this error messages are going to display. If 
                     registration was successfull it will return a JSON object with some meta data about the successfull completion of registraion as well as a linke where the user will be redirected to
                     The JSON object looks like the following ony contains different values, depending on what kind of error or success
                     result[1] = {                                  
                            'status'                 : False,       # False if an error occured, True if everything went as planned
                            'status-code'            : None,        # Contains an status code
                            'status-description'     : None,        # contains a description about the current status
                            'redirect-status'        : False,       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
                            'redirect-target'        : None,        # Contains the URL where user will be redirected if redirection is enabled (true)
                            'display-messages'       : None,        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
                            'display-messages-target': None         # Contains the HTML Id from the wrapper div-box where the message will be displayed
                        }

    Tests:
        * Test if it secure against Java Script code that is entered into the HTML input fields and could mainpulate our databases
        * Verify that it is not possible to register more than one time with the same email address
        * Test the case that user diable javascript in his browser           
    """


    method = request.method
    args   = request.form
    if method == 'POST':
        i                   = 1
        validation          = Validation()
        error_handling_form = FormError()
        result              = {}
        result[1]           = {                                                     
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }            

        # -------------------------------------------------------------------------------------------------------
        # validate that firstname is set and is not empty
        if not 'firstname' in args or validation.validation_isEmpty(args['firstname']) or 'firstname' == None:
            i             = i+1
            firstname_err = (error_handling_form.formError_invalidLength('#Firstname','', '', 'Please enter your Firstname!'))
            result[i]     = firstname_err['Invalid-Empty-String']

        # validate that firstname contains letters only
        elif validation.validation_isAlpha(args['firstname']) == False:
            i             = i+1
            firstname_err = (error_handling_form.formError_invalidTypeError('#Firstname', 'Firstname', '', 'letters from a-z or A-Z! Spaces are not allowed'))
            result[i]     = firstname_err['Invalid-Arguments']

        # validate that firstname has at least 2 Charactes
        elif validation.validation_minLength(args['firstname'], 2) == False:
            i             = i+1
            firstname_err = (error_handling_form.formError_invalidLength('#Firstname', '2', 'Firstname', ''))
            result[i]     = firstname_err['Invalid-Minimum-Of-Length']

        # -------------------------------------------------------------------------------------------------------
        # validate that lastname is set an is not empty
        if not 'lastname' in args or validation.validation_isEmpty(args['lastname']) or 'lastname' == None:
            i            = i+1
            lastname_err = (error_handling_form.formError_invalidLength('#Lastname', '', '', 'Please enter your Lastname!'))
            result[i]    = lastname_err['Invalid-Empty-String']

        # validate that lastname contains letters only
        elif validation.validation_isAlpha(args['lastname']) == False:
            i            = i+1
            lastname_err = (error_handling_form.formError_invalidTypeError('#Lastname', 'Lastname', '', 'letters from a-z or A-Z! Spaces are not allowed'))
            result[i]    = lastname_err['Invalid-Arguments']
        
        # validate that lastname has at least 2 Charactes
        elif validation.validation_minLength(args['lastname'], 2) == False:
            i            = i+1
            lastname_err = (error_handling_form.formError_invalidLength('#Lastname', '2', 'Lastname', ''))
            result[i]    = lastname_err['Invalid-Minimum-Of-Length']
        
        
        # -------------------------------------------------------------------------------------------------------
        # validate that email is set and is not empty
        if not 'email' in args or validation.validation_isEmpty(args['email']) or 'email' == None:
            i         = i+1
            email_err = (error_handling_form.formError_invalidLength('#Email', '', '', 'Please enter your E-Mail Address!'))
            result[i] = email_err['Invalid-Empty-String']

        # validate that email has a valid email format
        elif validation.validation_isEmail(args['email']) == False:
            i         = i+1
            email_err = (error_handling_form.formError_invalidEmail('#Email'))
            result[i] = email_err['Invalid-Format']
        
        
        # -------------------------------------------------------------------------------------------------------
        # validate that password is set and is not empty
        if not 'pwd' in args or validation.validation_isEmpty(args['pwd']) or 'pwd' == None:
            i         = i+1
            pwd_err   = (error_handling_form.formError_invalidLength('#Password', '', '', 'Please enter a Password!'))
            result[i] = pwd_err['Invalid-Empty-String']

        # validate that password contains at least 8 characters
        elif validation.validation_minLength(args['pwd'], 8) == False:
            i         = i+1
            pwd_err   = (error_handling_form.formError_invalidLength('#Password', '8', 'Password', ''))
            result[i] = pwd_err['Invalid-Maximum-Of-Length']

        # validate that password contains at least one upper character
        elif validation.validation_containsUpperChar(args['pwd']) == False:
            i         = i+1
            pwd_err   = (error_handling_form.formError_invalidTypeError('#Password', 'Password', '', 'one upper character'))
            result[i] = pwd_err['Missing-Arguments']

        # validte that password contains at least one lower charaacter
        elif validation.validation_containsLowerChar(args['pwd']) == False:
            i         = i+1
            pwd_err   = (error_handling_form.formError_invalidTypeError('#Password', 'Password', '', 'one lower character'))
            result[i] = pwd_err['Missing-Arguments']

        # validate that password contains at least one digit
        elif validation.validation_containsDigit(args['pwd']) == False:
            i         = i+1
            pwd_err   = (error_handling_form.formError_invalidTypeError('#Password', 'Password', '', 'one number'))
            result[i] = pwd_err['Missing-Arguments']

        # validate that password contains at least one special character
        elif validation.validation_containsSpecialChar(args['pwd']) == False:
            i         = i+1
            pwd_err   = (error_handling_form.formError_invalidTypeError('#Password', 'Password', '', 'one special character'))
            result[i] = pwd_err['Missing-Arguments']

        # validate that password does not contain firstname, lastname, email or 'admin', 'adm', 'administrator'
        elif validation.validation_followPasswordRequlations(args['pwd'], args['firstname'], args['lastname'], args['email']):
            i         = i+1
            pwd_err   = (error_handling_form.formError_invalidPassword('#Password'))
            result[i] = pwd_err['Invalid-Format']
        
        
        # -------------------------------------------------------------------------------------------------------
        # validate that user entered text to confirm his password 
        if not 'confirm-pwd' in args or validation.validation_isEmpty(args['confirm-pwd']) or 'confirm-pwd' == None:
            i               = i+1
            confrim_pwd_err = (error_handling_form.formError_invalidLength('#Confirm-Password', '', '', 'Please confirm your Password!'))
            result[i]       = confrim_pwd_err['Invalid-Empty-String']

        # validate that password and confirmation password machtes 
        elif  args['confirm-pwd'] != args['pwd']:
            i               = i + 1
            confrim_pwd_err = (error_handling_form.formError_invalidPassword('#Confirm-Password'))
            result[i]       = confrim_pwd_err['Confirmation-Error']
        
        # -------------------------------------------------------------------------------------------------------
        # validate that no error was set during the above validating process -> if i = 1 -> no errors occured
        if i == 1:
            user       = User()
            tmp_result = user.user_register(args)        
            
            if tmp_result:                                                                                          # if there were no errors, the user gets registerd whith this function written in user.py
                result[1]['status']                  = True
                result[1]['status-code']             = 200
                result[1]['status-description']      = 'OK'
                result[1]['redirect-status']         = True
                result[1]['redirect-target']         = 'http://127.0.0.1:5000/auth/registerd-successfull?status=true'
                result[1]['display-messages']        = None
                result[1]['display-messages-target'] = None
                return result                                                                                       # result is true if user data could be written to the db successfully
            
            else:
                error_handling_db                    = DbError()
                result[1]['status']                  = False
                result[1]['status-code']             = 404
                result[1]['status-description']      = 'Error'
                result[1]['redirect-status']         = False
                result[1]['redirect-target']         = None
                result[1]['display-messages']        = 'inpage-alert'
                result[1]['display-messages-target'] = '#Register-Feedback-Error-Wrapper'

                
                # error handling in case no results were found
                if user.Error == '1':
                    tmp_error = (error_handling_db.dbError_noResultFound('#Register-Feedback-Error'))
                    result[2] = tmp_error['No-User-Found']
                    return result
                
                # error handling in case email is already existing
                elif user.Error == '2':
                    tmp_error = (error_handling_db.dbError_IntegrityError('#Register-Feedback-Error'))
                    result[2] = tmp_error['Multiple-Users-Found']
                    return result

                # error handling in case of an compile error
                elif user.Error == '3':
                    tmp_error = (error_handling_db.dbError_CompileError('#Register-Feedback-Error'))
                    result[2] = tmp_error['Compile-Error']
                    return result

                # error handling in case of a DBAPI error
                elif user.Error == '4':
                    tmp_error = (error_handling_db.dbError_DBAPIError('#Register-Feedback-Error'))
                    result[2] = tmp_error['DBAPI-Error']
                    return result
                
                # error handling in case of some other internal errors or problems
                elif user.Error == '5':
                    tmp_error = (error_handling_db.dbError_InternalError('#Register-Feedback-Error'))
                    result[2] = tmp_error['Internal-Error']
                    return result
                
                # error handling in case that more than one result were found
                elif user.Error == '6':
                    tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Register-Feedback-Error'))
                    result[2] = tmp_error['Multi-User-Found']
                    return result
                
                # error handling in case of an missing reference table error
                elif user.Error == '7':
                    tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Register-Feedback-Error'))
                    result[2] = tmp_error['No-Referenced-Table'] 
                    return result
                
                # error handling in case that object is not executable
                elif user.Error == '8':
                    tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Register-Feedback-Error'))
                    result[2] = tmp_error['Object-Not-Executable']
                    return result
                
                # error handling in case of other sqlalchmey errors
                elif user.Error == '9':
                    tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Register-Feedback-Error'))
                    result[2] = tmp_error['SQL-Alchemy-Error']
                    return result
        return result






# --------------------------------------------------------------------------------------
# API Interface to log User in
# --------------------------------------------------------------------------------------
@api.route('/log-user-in', methods=['POST'])
def api_login():
    """
    This method is used to validate that all necessary data needed to log user in are provided by the user. The both input fields User-Email and User-Password will be validated that it only containts data of the right format.
    This method will also call the user_login function to connect to the database gets the corresponding user for the email that has been entered by the user to the login form. Before returning the user data from the database
    and store it into the flask_login modul, the data will be validated first. 
    * E-Mail Address
        * isEmpty: will add an Error to the JSON object if no email address is provided
        * isEmail: will add an Error to the JSON object if email has no valid email format

    * Password
        * isEmpty: will add an Error to the JSON object if no password is provided

    Args:
        * email (String)   : this contains the email address which the usere entered into the HTML form on the sign-in webpage to login
        * password (String): this contains the password the user entered into the HTML form on the sign-in webpage to log in

    Returns:
        JSON object: This method returns a JSON object that contains information about occured errors if login was not successfull as well as some metadata where this error messages are going to display. If 
                     login was successfull it will return a JSON object with some meta data about the successfull completion of lgoin as well as a linke where the user will be redirected to.
                     The JSON object looks like the following ony contains different values, depending on what kind of error or success
                     result[1] = {                                  
                            'status'                 : False,       # False if an error occured, True if everything went as planned
                            'status-code'            : None,        # Contains an status code
                            'status-description'     : None,        # contains a description about the current status
                            'redirect-status'        : False,       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
                            'redirect-target'        : None,        # Contains the URL where user will be redirected if redirection is enabled (true)
                            'display-messages'       : None,        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
                            'display-messages-target': None         # Contains the HTML Id from the wrapper div-box where the message will be displayed
                        }
    Tests:
        * Validate that flask-login works well without any problemes and that the information about the loged in user is right and properly stored in seesions
        * Validate that user can only log in if the user has the right credentials and that password verifying works well
    """



    method = request.method
    args   = request.form
    if method == 'POST':
        i                   = 1
        validation          = Validation()
        error_handling_form = FormError()
        result              = {}
        result[1]           = {
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }            

        # -------------------------------------------------------------------------------------------------------
        # validate that email is set and is not empty
        if not 'email' in args or validation.validation_isEmpty(args['email']) or 'email' == None:
            i         = i+1
            email_err = (error_handling_form.formError_invalidLength('#Email', '', '', 'Please enter your E-Mail Address!'))
            result[i] = email_err['Invalid-Empty-String']

        # validate that email has a valid email format
        elif validation.validation_isEmail(args['email']) == False:
            i         = i+1
            email_err = (error_handling_form.formError_invalidEmail('#Email'))
            result[i] = email_err['Invalid-Format']

        # -------------------------------------------------------------------------------------------------------
        # validate that password is set and is not empty
        if not 'pwd' in args or validation.validation_isEmpty(args['pwd']) or 'pwd' == None:
            i         = i+1
            pwd_err   = (error_handling_form.formError_invalidLength('#Password', '', '', 'Please enter your Password!'))
            result[i] = pwd_err['Invalid-Empty-String']
        
        # -------------------------------------------------------------------------------------------------------
        # validate that no error was set during the above validating process -> if i = 1 -> no errors occured
        if i == 1:
            user       = User()
            tmp_result = user.user_login(args)                                                                          # if there were no errors, the user gets registerd whith this function written in user.py
            
            if tmp_result:                                                                                              # result is true if user data could be written to the db successfully 
                if user.LoggedIn:                                                                                       # validate that login was successfull
                    result[1]['status']                  = True
                    result[1]['status-code']             = 200
                    result[1]['status-description']      = 'OK'
                    result[1]['redirect-status']         = True
                    result[1]['redirect-target']         = 'http://127.0.0.1:5000/dashboard'
                    result[1]['display-messages']        = None
                    result[1]['display-messages-target'] = None
                return result                                                                                           # result is true if user data could be written to the db successfully
            
            else:                                                                                                       # if login was not successfull as a result of a Database Failure
                error_handling_db                     = DbError()
                result[1]['status']                   = False
                result[1]['status-code']              = 404
                result[1]['status-description']       = 'Error'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = None
                result[1]['display-messages']         = 'inpage-alert'
                result[1]['display-messages-target'] = '#Login-Feedback-Error-Wrapper'


                # error handling in case no results were found
                if user.Error == '1':
                    tmp_error = (error_handling_db.dbError_noResultFound('#Login-Feedback-Error'))
                    result[2] = tmp_error['No-User-Found']
                    return result
                
                # error handling in case email is already existing
                elif user.Error == '2':
                    tmp_error = (error_handling_db.dbError_IntegrityError('#Login-Feedback-Error'))
                    result[2] = tmp_error['Multiple-Users-Found']
                    return result

                # error handling in case of an compile error
                elif user.Error == '3':
                    tmp_error = (error_handling_db.dbError_CompileError('#Login-Feedback-Error'))
                    result[2] = tmp_error['Compile-Error']
                    return result

                # error handling in case of a DBAPI error
                elif user.Error == '4':
                    tmp_error = (error_handling_db.dbError_DBAPIError('#Login-Feedback-Error'))
                    result[2] = tmp_error['DBAPI-Error']
                    return result
                
                # error handling in case some other internal errors or problems
                elif user.Error == '5':
                    tmp_error = (error_handling_db.dbError_InternalError('#Login-Feedback-Error'))
                    result[2] = tmp_error['Internal-Error']
                    return result
                
                # error handling in case that more than one result were found
                elif user.Error == '6':
                    tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Login-Feedback-Error'))
                    result[2] = tmp_error['Multi-User-Found']
                    return result
                
                # error handling in case of an missing reference table error
                elif user.Error == '7':
                    tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Login-Feedback-Error'))
                    result[2] = tmp_error['No-Referenced-Table']
                    return result
                
                # error handling in case that object is not executable
                elif user.Error == '8':
                    tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Login-Feedback-Error'))
                    result[2] = tmp_error['Object-Not-Executable']
                    return result
                
                # error handling in case of other sqlalchmey errors
                elif user.Error == '9':
                    tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Login-Feedback-Error'))
                    result[2] = tmp_error['SQL-Alchemy-Error']
                    return result

                # error handling in case that user credentials were wrong
                elif user.Error == '10':
                    tmp_error                            = (error_handling_form.formError_invalidPassword('#Login-Feedback-Error'))
                    result[1]['display-messages-target'] = '#Invalid-User-Credentials'
                    result[2]                            = tmp_error['Login-Error']
                    return result
        
        return result





# --------------------------------------------------------------------------------------
# API Interface to get all existing projects
# --------------------------------------------------------------------------------------
@api.route('get-all-projects', methods=['GET'])
def api_getAllProjects():
    """
    This method is used to get all projects that are stored in the database, convert them into a formated JSON object, and return it to the client, which sent the request to this API. During this process, errorhandling will also be established,
    in case of some database failure or errors.

    Args:
        * Contains or uses no Arguments

    Returns:
        * JSON object: This method will return a JSON object list with all projects that are available in the databasetable tbl_project_list

    Tests:
        * test that databse connection can be established
        * test stability and performance if database contains a huge amout of projects such as hundred thousands of projects
    """

    method = request.method
    if method == 'GET':
        result              = {}
        result[1]           = {
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }            

        project = Project()
        tmp     = project.project_getAllProjects()                                  # If there was no DB Error when selecting Projects, the variable will be true
            
        if tmp:
            result [1]['status']                   = True
            result [1]['status-code']              = 200
            result [1]['status-description']       = 'OK'
            result [1]['redirect-status']          = True
            result [1]['redirect-target']          = 'http://127.0.0.1:5000/dashboard'
            result [1]['display-messages']         = None
            result [1]['display-messages-target '] = None

            
            return jsonify({
                'status'          : result[1],
                'count-result-set': project.NumResult,
                'result-set-data' : project.Result
            })

        else:
            error_handling_db                      = DbError()
            result [1]['status']                   = False
            result [1]['status-code']              = 404
            result [1]['status-description']       = 'Error'
            result [1]['redirect-status']          = False
            result [1]['redirect-target']          = None
            result [1]['display-messages']         = 'inpage-alert'
            result [1]['display-messages-target '] = '#Project-Feedback-Error-Wrapper'

            # error handling in case no results were found
            if project.Error == '1':
                tmp_error = (error_handling_db.dbError_noResultFound('#Project-Feedback'))
                result[3] = tmp_error['No-Result-Found']
                return result
                
            # error handling in case email is already existing
            elif project.Error == '2':
                tmp_error = (error_handling_db.dbError_IntegrityError('#Project-Feedback'))
                result[3] = tmp_error['Multiple-Records-Found']
                return result

            # error handling in case of an compile error
            elif project.Error == '3':
                tmp_error = (error_handling_db.dbError_CompileError('#Project-Feedback'))
                result[3] = tmp_error['Compile-Error']
                return result

            # error handling in case of a DBAPI error
            elif project.Error == '4':
                tmp_error = (error_handling_db.dbError_DBAPIError('#Project-Feedback'))
                result[3] = tmp_error['DBAPI-Error']
                return result
                
            # error handling in case some other internal errors or problems
            elif project.Error == '5':
                tmp_error = (error_handling_db.dbError_InternalError('#Project-Feedback'))
                result[3] = tmp_error['Internal-Error']
                return result
                
            # error handling in case that more than one result were found
            elif project.Error == '6':
                tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Project-Feedback'))
                result[3] = tmp_error['Multi-Records-Found']
                return result
                
            # error handling in case of an missing reference table error
            elif project.Error == '7':
                tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Project-Feedback'))
                result[3] = tmp_error['No-Referenced-Table']
                return result
                
            # error handling in case that object is not executable
            elif project.Error == '8':
                tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Project-Feedback'))
                result[3] = tmp_error['Object-Not-Executable']
                return result
                
            # error handling in case of other sqlalchmey errors
            elif project.Error == '9':
                tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Project-Feedback'))
                result[3] = tmp_error['SQL-Alchemy-Error']
                return result





# --------------------------------------------------------------------------------------
# API Interface to get all existing projects that belongs to the loged in user
# --------------------------------------------------------------------------------------
@api.route('/get-all-projects-by-user', methods=['GET'])
def api_getAllProjectsByUser():
    """
    This method is used to get all projects that belongs to a specific user and that are stored in the database table tbl_project_list, convert them into a formated JSON object, and return it to the client, which sent the request to this API.
    During this process, errorhandling will also be established in case of some database failure or errors.

    Args:
        * user-id (Integer): When sending a request to the api.rout(/get-all-projects-by-user), a user id has to be send within the request, otherwise it is not possible to get only the projects, that belongs to a specific user.

    Returns:
        * JSON object: This method will return a JSON object list, with all projects that belongs to the spcific user, from which the user-id was given and are available in the databasetable tbl_project_list

    Test:
        * test what will happen, if an string or char is given with the request to identify the users project, instead of an interger
        * test what will happen if an user id is given with the request which does not exists in the user table tbl_user_list
    """

    method = request.method
    args   = request.args

    if method == 'GET':
        i                   = 1
        validation          = Validation()
        error_handling_form = FormError()
        result              = {}
        result[1]           = {
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }            

        # -------------------------------------------------------------------------------------------------------
        # validate that user-id is set and is not empty
        if not 'user-id' in args or validation.validation_isEmpty(args['user-id']) or 'user-id' == None:
            i           = i+1
            user_id_err = (error_handling_form.formError_invalidLength('#Project-Feedback', '', '', 'Please validate that an user is logged in to get user projects!'))
            result[i]   = user_id_err['Invalid-Empty-String']
        # -------------------------------------------------------------------------------------------------------
        # validate that no error was set during the above validating process -> if i = 1 -> no errors occured
        if i == 1:
            user_id    = args['user-id']
            project    = Project()
            tmp_result = project.project_getAllProjectsByUser(user_id)


            if tmp_result:
                result[1]['status']                   = True
                result[1]['status-code']              = 200
                result[1]['status-description']       = 'OK'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = 'http://127.0.0.1:5000/dashboard'
                result[1]['display-messages']         = None
                result[1]['display-messages-target '] = None

                return jsonify({
                    'status'          : result[1],
                    'count-result-set': project.NumResult,
                    'result-set-data' : project.Result
                })

            else:
                error_handling_db                     = DbError()
                result[1]['status']                   = False
                result[1]['status-code']              = 404
                result[1]['status-description']       = 'Error'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = None
                result[1]['display-messages']         = False
                result[1]['display-messages-target '] = None


                # error handling in case no results were found
                if project.Error == '1':
                    tmp_error = (error_handling_db.dbError_noResultFound('#Project-Feedback'))
                    result[2] = tmp_error['No-Result-Found']
                    return result
                    
                # error handling in case email is already existing
                elif project.Error == '2':
                    tmp_error = (error_handling_db.dbError_IntegrityError('#Project-Feedback'))
                    result[2] = tmp_error['Multiple-Records-Found']
                    return result

                # error handling in case of an compile error
                elif project.Error == '3':
                    tmp_error = (error_handling_db.dbError_CompileError('#Project-Feedback'))
                    result[2] = tmp_error['Compile-Error']
                    return result

                # error handling in case of a DBAPI error
                elif project.Error == '4':
                    tmp_error = (error_handling_db.dbError_DBAPIError('#Project-Feedback'))
                    result[2] = tmp_error['DBAPI-Error']
                    return result
                    
                # error handling in case of some other internal errors or problems
                elif project.Error == '5':
                    tmp_error = (error_handling_db.dbError_InternalError('#Project-Feedback'))
                    result[2] = tmp_error['Internal-Error']
                    return result
                    
                # error handling in case that more than one result were found
                elif project.Error == '6':
                    tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Project-Feedback'))
                    result[2] = tmp_error['Multi-Records-Found']
                    return result
                    
                # error handling in case of an missing reference table error
                elif project.Error == '7':
                    tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Project-Feedback'))
                    result[2] = tmp_error['No-Referenced-Table']
                    return result
                    
                # error handling in case that object is not executable
                elif project.Error == '8':
                    tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Project-Feedback'))
                    result[2] = tmp_error['Object-Not-Executable']
                    return result
                    
                # error handling in case of other sqlalchmey errors
                elif project.Error == '9':
                    tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Project-Feedback'))
                    result[2] = tmp_error['SQL-Alchemy-Error']
                    return result




# --------------------------------------------------------------------------------------
# API Interface to get a specific project that belongs to the loged in user
# --------------------------------------------------------------------------------------
@api.route('get-single-project-by-users-project-id', methods=['GET'])
def api_getSingleProjectByUser():
    """
    This function is used to 

    Returns:
        [type]: [description]
    """

    method = request.method
    args   = request.args

    if method == 'GET':
        i                   = 1
        validation          = Validation()
        error_handling_form = FormError()
        result              = {}
        result[1]           = {
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }

        # -------------------------------------------------------------------------------------------------------
        # validate that user-id is set and is not empty
        if not 'user-id' in args or validation.validation_isEmpty(args['user-id']) or 'user-id' == None:
            i           = i+1
            user_id_err = (error_handling_form.formError_invalidLength('#Project-Feedback', '', '', 'Please validate that an user is logged in to get user projects!'))
            result[i]   = user_id_err['Invalid-Empty-String']
        # -------------------------------------------------------------------------------------------------------
        # validate that project-id is set and is not empty
        if not 'project-id' in args or validation.validation_isEmpty(args['project-id']) or 'project-id' == None:
            i              = i+1
            project_id_err = (error_handling_form.formError_invalidLength('#Project-Feedback','', '', 'Please validate that an Project Id is set to identify the required project!'))
            result[i]      = project_id_err['Invalid-Empty-String']

        # -------------------------------------------------------------------------------------------------------
        # validate that no error was set during the above validating process -> if i = 1 -> no errors occured
        if i == 1:
            user_id    = args['user-id']
            project_id = args['project-id']

            project    = Project()
            tmp_result = project.project_getProjectByProjectId(user_id, project_id)


            if tmp_result:
                result[1]['status']                   = True
                result[1]['status-code']              = 200
                result[1]['status-description']       = 'OK'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = 'http://127.0.0.1:5000/dashboard'
                result[1]['display-messages']         = None
                result[1]['display-messages-target '] = None

                return jsonify({
                    'status'          : result[1],
                    'count-result-set': project.NumResult,
                    'result-set-data' : project.Result
                })

            else:
                error_handling_db                     = DbError()
                result[1]['status']                   = False
                result[1]['status-code']              = 404
                result[1]['status-description']       = 'Error'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = None
                result[1]['display-messages']         = False
                result[1]['display-messages-target '] = None


                 # error handling in case no results were found
                if project.Error == '1':
                    tmp_error = (error_handling_db.dbError_noResultFound('#Project-Feedback'))
                    result[2] = tmp_error['No-Result-Found']
                    return result
                    
                # error handling in case email is already existing
                elif project.Error == '2':
                    tmp_error = (error_handling_db.dbError_IntegrityError('#Project-Feedback'))
                    result[2] = tmp_error['Multiple-Records-Found']
                    return result

                # error handling in case of an compile error
                elif project.Error == '3':
                    tmp_error = (error_handling_db.dbError_CompileError('#Project-Feedback'))
                    result[2] = tmp_error['Compile-Error']
                    return result

                # error handling in case of a DBAPI error
                elif project.Error == '4':
                    tmp_error = (error_handling_db.dbError_DBAPIError('#Project-Feedback'))
                    result[2] = tmp_error['DBAPI-Error']
                    return result
                    
                # error handling in case of some other internal errors or problems
                elif project.Error == '5':
                    tmp_error = (error_handling_db.dbError_InternalError('#Project-Feedback'))
                    result[2] = tmp_error['Internal-Error']
                    return result
                    
                # error handling in case that more than one result were found
                elif project.Error == '6':
                    tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Project-Feedback'))
                    result[2] = tmp_error['Multi-Records-Found']
                    return result
                    
                # error handling in case of an missing reference table error
                elif project.Error == '7':
                    tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Project-Feedback'))
                    result[2] = tmp_error['No-Referenced-Table']
                    return result
                    
                # error handling in case that object is not executable
                elif project.Error == '8':
                    tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Project-Feedback'))
                    result[2] = tmp_error['Object-Not-Executable']
                    return result
                    
                # error handling in case of other sqlalchmey errors
                elif project.Error == '9':
                    tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Project-Feedback'))
                    result[2] = tmp_error['SQL-Alchemy-Error']
                    return result

        return result






# --------------------------------------------------------------------------------------
# API Interface to get the date difference from project-start-date to project-end-date
# --------------------------------------------------------------------------------------
@api.route('/get-date-difference-ste-by-project-id', methods=['GET'])
def api_getNumberObfDaysFromStartToEndByProjectId():
    """
    This method is used to get date difference between the project end date and the project start date, which means that this method will call the project database method wich caclulates the amount of days between project start date and project end date.
    To do so, a specific project id is required.
    """


    method = request.method
    args   = request.args

    if method == 'GET':
        i                   = 1
        validation          = Validation()
        error_handling_form = FormError()
        result              = {}
        result[1]           = {
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }   

        # -------------------------------------------------------------------------------------------------------
        # validate that user-id is set and is not empty
        if not 'user-id' in args or validation.validation_isEmpty(args['user-id']) or 'user-id' == None:
            i           = i+1
            user_id_err = (error_handling_form.formError_invalidLength('#Project-Feedback', '', '', 'Please validate that an user is logged in to identify user project!'))
            result[i]   = user_id_err['Invalid-Empty-String']

        # -------------------------------------------------------------------------------------------------------
        # validate that project-id is set and is not empty
        if not 'project-id' in args or validation.validation_isEmpty(args['project-id']) or 'project-id' == None:
            i              = i+1
            project_id_err = (error_handling_form.formError_invalidLength('#Project-Feedback','', '', 'Please validate that an Project Id is set to identify the required project!'))
            result[i]      = project_id_err['Invalid-Empty-String']

        # -------------------------------------------------------------------------------------------------------
        # validate that no error was set during the above validating process -> if i = 1 -> no errors occured
        if i == 1:
            user_id    = args['user-id']
            project_id = args['project-id']
            
            project    = Project()
            tmp_result = project.project_getNumberOfDaysFromStartToEndByProjectId(user_id, project_id)
            

            if tmp_result:
                result[1]['status']                   = True
                result[1]['status-code']              = 200
                result[1]['status-description']       = 'OK'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = 'http://127.0.0.1:5000/dashboard'
                result[1]['display-messages']         = None
                result[1]['display-messages-target '] = None

                return jsonify({
                    'status'          : result[1],
                    'count-result-set': project.NumResult,
                    'result-set-data' : project.Result
                })

            else:
                error_handling_db                     = DbError()
                result[1]['status']                   = False
                result[1]['status-code']              = 404
                result[1]['status-description']       = 'Error'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = None
                result[1]['display-messages']         = False
                result[1]['display-messages-target '] = None


                 # error handling in case no results were found
                if project.Error == '1':
                    tmp_error = (error_handling_db.dbError_noResultFound('#Project-Feedback'))
                    result[2] = tmp_error['No-Result-Found']
                    return result
                    
                # error handling in case email is already existing
                elif project.Error == '2':
                    tmp_error = (error_handling_db.dbError_IntegrityError('#Project-Feedback'))
                    result[2] = tmp_error['Multiple-Records-Found']
                    return result

                # error handling in case of an compile error
                elif project.Error == '3':
                    tmp_error = (error_handling_db.dbError_CompileError('#Project-Feedback'))
                    result[2] = tmp_error['Compile-Error']
                    return result

                # error handling in case of a DBAPI error
                elif project.Error == '4':
                    tmp_error = (error_handling_db.dbError_DBAPIError('#Project-Feedback'))
                    result[2] = tmp_error['DBAPI-Error']
                    return result
                    
                # error handling in case of some other internal errors or problems
                elif project.Error == '5':
                    tmp_error = (error_handling_db.dbError_InternalError('#Project-Feedback'))
                    result[2] = tmp_error['Internal-Error']
                    return result
                    
                # error handling in case that more than one result were found
                elif project.Error == '6':
                    tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Project-Feedback'))
                    result[2] = tmp_error['Multi-Records-Found']
                    return result
                    
                # error handling in case of an missing reference table error
                elif project.Error == '7':
                    tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Project-Feedback'))
                    result[2] = tmp_error['No-Referenced-Table']
                    return result
                    
                # error handling in case that object is not executable
                elif project.Error == '8':
                    tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Project-Feedback'))
                    result[2] = tmp_error['Object-Not-Executable']
                    return result
                    
                # error handling in case of other sqlalchmey errors
                elif project.Error == '9':
                    tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Project-Feedback'))
                    result[2] = tmp_error['SQL-Alchemy-Error']
                    return result






# --------------------------------------------------------------------------------------
# API Interface to get the date difference from project-start-date to todays date
# --------------------------------------------------------------------------------------
@api.route('/get-date-difference-stt-by-project-id', methods=['GET'])
def api_getNumberOfDaysFromStartToTodayByPorjectId():
    """
    This method is used to 
    """
             
    method = request.method
    args   = request.args

    if method == 'GET':
        i                   = 1
        validation          = Validation()
        error_handling_form = FormError()
        result              = {}
        result[1]           = {
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }   


        # -------------------------------------------------------------------------------------------------------
        # validate that user-id is set and is not empty
        if not 'user-id' in args or validation.validation_isEmpty(args['user-id']) or 'user-id' == None:
            i           = i+1
            user_id_err = (error_handling_form.formError_invalidLength('#Project-Feedback', '', '', 'Please validate that an user is logged in to identify user project!'))
            result[i]   = user_id_err['Invalid-Empty-String']

        # -------------------------------------------------------------------------------------------------------
        # validate that project-id is set and is not empty
        if not 'project-id' in args or validation.validation_isEmpty(args['project-id']) or 'project-id' == None:
            i              = i+1
            project_id_err = (error_handling_form.formError_invalidLength('#Project-Feedback','', '', 'Please validate that an Project Id is set to identify the required project!'))
            result[i]      = project_id_err['Invalid-Empty-String']

        # -------------------------------------------------------------------------------------------------------
        # validate that no error was set during the above validating process -> if i = 1 -> no errors occured
        if i == 1:
            user_id    = args['user-id']
            project_id = args['project-id']

            project    = Project()
            tmp_result = project.project_getNumberOfDaysFromStartToTodayByProjectId(user_id, project_id)


            if tmp_result:
                result[1]['status']                   = True
                result[1]['status-code']              = 200
                result[1]['status-description']       = 'OK'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = 'http://127.0.0.1:5000/dashboard'
                result[1]['display-messages']         = None
                result[1]['display-messages-target '] = None

                return jsonify({
                    'status'          : result[1],
                    'count-result-set': project.NumResult,
                    'result-set-data' : project.Result
                })

            else:
                error_handling_db                     = DbError()
                result[1]['status']                   = False
                result[1]['status-code']              = 404
                result[1]['status-description']       = 'Error'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = None
                result[1]['display-messages']         = False
                result[1]['display-messages-target '] = None


                 # error handling in case no results were found
                if project.Error == '1':
                    tmp_error = (error_handling_db.dbError_noResultFound('#Project-Feedback'))
                    result[2] = tmp_error['No-Result-Found']
                    return result
                    
                # error handling in case email is already existing
                elif project.Error == '2':
                    tmp_error = (error_handling_db.dbError_IntegrityError('#Project-Feedback'))
                    result[2] = tmp_error['Multiple-Records-Found']
                    return result

                # error handling in case of an compile error
                elif project.Error == '3':
                    tmp_error = (error_handling_db.dbError_CompileError('#Project-Feedback'))
                    result[2] = tmp_error['Compile-Error']
                    return result

                # error handling in case of a DBAPI error
                elif project.Error == '4':
                    tmp_error = (error_handling_db.dbError_DBAPIError('#Project-Feedback'))
                    result[2] = tmp_error['DBAPI-Error']
                    return result
                    
                # error handling in case of some other internal errors or problems
                elif project.Error == '5':
                    tmp_error = (error_handling_db.dbError_InternalError('#Project-Feedback'))
                    result[2] = tmp_error['Internal-Error']
                    return result
                    
                # error handling in case that more than one result were found
                elif project.Error == '6':
                    tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Project-Feedback'))
                    result[2] = tmp_error['Multi-Records-Found']
                    return result
                    
                # error handling in case of an missing reference table error
                elif project.Error == '7':
                    tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Project-Feedback'))
                    result[2] = tmp_error['No-Referenced-Table']
                    return result
                    
                # error handling in case that object is not executable
                elif project.Error == '8':
                    tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Project-Feedback'))
                    result[2] = tmp_error['Object-Not-Executable']
                    return result
                    
                # error handling in case of other sqlalchmey errors
                elif project.Error == '9':
                    tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Project-Feedback'))
                    result[2] = tmp_error['SQL-Alchemy-Error']
                    return result






# --------------------------------------------------------------------------------------
# API Interface to get the date difference from todays date to project-end-date
# --------------------------------------------------------------------------------------
@api.route('/get-date-difference-tte-by-project-id', methods=['GET'])
def api_getNumberOfDaysFromTodayToEndByProjectId():
    """
    This method is used to
    """

    method = request.method
    args   = request.args

    if method == 'GET':
        i                   = 1
        validation          = Validation()
        error_handling_form = FormError()
        result              = {}
        result[1]           = {
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }   


        # -------------------------------------------------------------------------------------------------------
        # validate that user-id is set and is not empty
        if not 'user-id' in args or validation.validation_isEmpty(args['user-id']) or 'user-id' == None:
            i           = i+1
            user_id_err = (error_handling_form.formError_invalidLength('#Project-Feedback', '', '', 'Please validate that an user is logged in to identify user project!'))
            result[i]   = user_id_err['Invalid-Empty-String']

        # -------------------------------------------------------------------------------------------------------
        # validate that project-id is set and is not empty
        if not 'project-id' in args or validation.validation_isEmpty(args['project-id']) or 'project-id' == None:
            i              = i+1
            project_id_err = (error_handling_form.formError_invalidLength('#Project-Feedback','', '', 'Please validate that an Project Id is set to identify the required project!'))
            result[i]      = project_id_err['Invalid-Empty-String']

        # -------------------------------------------------------------------------------------------------------
        # validate that no error was set during the above validating process -> if i = 1 -> no errors occured
        if i == 1:
            user_id    = args['user-id']
            project_id = args['project-id']

            project    = Project()
            tmp_result = project.project_getNumberOfDaysFromTodayToEndByProjectId(user_id, project_id)


            if tmp_result:
                result[1]['status']                   = True
                result[1]['status-code']              = 200
                result[1]['status-description']       = 'OK'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = 'http://127.0.0.1:5000/dashboard'
                result[1]['display-messages']         = None
                result[1]['display-messages-target '] = None

                return jsonify({
                    'status'          : result[1],
                    'count-result-set': project.NumResult,
                    'result-set-data' : project.Result
                })

            else:
                error_handling_db                     = DbError()
                result[1]['status']                   = False
                result[1]['status-code']              = 404
                result[1]['status-description']       = 'Error'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = None
                result[1]['display-messages']         = False
                result[1]['display-messages-target '] = None


                 # error handling in case no results were found
                if project.Error == '1':
                    tmp_error = (error_handling_db.dbError_noResultFound('#Project-Feedback'))
                    result[2] = tmp_error['No-Result-Found']
                    return result
                    
                # error handling in case email is already existing
                elif project.Error == '2':
                    tmp_error = (error_handling_db.dbError_IntegrityError('#Project-Feedback'))
                    result[2] = tmp_error['Multiple-Records-Found']
                    return result

                # error handling in case of an compile error
                elif project.Error == '3':
                    tmp_error = (error_handling_db.dbError_CompileError('#Project-Feedback'))
                    result[2] = tmp_error['Compile-Error']
                    return result

                # error handling in case of a DBAPI error
                elif project.Error == '4':
                    tmp_error = (error_handling_db.dbError_DBAPIError('#Project-Feedback'))
                    result[2] = tmp_error['DBAPI-Error']
                    return result
                    
                # error handling in case of some other internal errors or problems
                elif project.Error == '5':
                    tmp_error = (error_handling_db.dbError_InternalError('#Project-Feedback'))
                    result[2] = tmp_error['Internal-Error']
                    return result
                    
                # error handling in case that more than one result were found
                elif project.Error == '6':
                    tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Project-Feedback'))
                    result[2] = tmp_error['Multi-Records-Found']
                    return result
                    
                # error handling in case of an missing reference table error
                elif project.Error == '7':
                    tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Project-Feedback'))
                    result[2] = tmp_error['No-Referenced-Table']
                    return result
                    
                # error handling in case that object is not executable
                elif project.Error == '8':
                    tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Project-Feedback'))
                    result[2] = tmp_error['Object-Not-Executable']
                    return result
                    
                # error handling in case of other sqlalchmey errors
                elif project.Error == '9':
                    tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Project-Feedback'))
                    result[2] = tmp_error['SQL-Alchemy-Error']
                    return result





# --------------------------------------------------------------------------------------
# API Interface to create a new project and asign it to the user loged in 
# --------------------------------------------------------------------------------------
@api.route('/create-project', methods=['POST'])
def api_createProject():
    """
    This function is used to create projects
    """
    method = request.method
    args   = request.form

    if method == 'POST':
        i                   = 1
        validation          = Validation()
        error_handling_form = FormError()
        result              = {}
        result[1]           = {
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }





        # -------------------------------------------------------------------------------------------------------
        # validate that project title is set and is not empty
        if not 'project-title' in args or validation.validation_isEmpty(args['project-title']) or 'project-title' == None:
            i                 = i+1
            project_title_err = (error_handling_form.formError_invalidLength('#Project-Title','', '', 'Please enter a Project Title!'))
            result[i]         = project_title_err['Invalid-Empty-String']

        # validate that project title contains letters only
        elif validation.validation_isAlphaWithSpaces(args['project-title']) == False:
            i                 = i+1
            project_title_err = (error_handling_form.formError_invalidTypeError('#Project-Title', 'Project Title', '', 'letters from a-z or A-Z! Spaces are not allowed'))
            result[i]         = project_title_err['Invalid-Arguments']

        # validate that project title has at least 2 Charactes
        elif validation.validation_minLength(args['project-title'], 2) == False:
            i                 = i+1
            project_title_err = (error_handling_form.formError_invalidLength('#Project-Title', '2', 'Project Title', ''))
            result[i]         = project_title_err['Invalid-Minimum-Of-Length'] 
            
        # validate that project title has not than more 75 Charactes
        elif validation.validation_maxLength(args['project-title'], 75) == False:
            i                 = i+1
            project_title_err = (error_handling_form.formError_invalidLength('#Project-Title', '75', 'Project Title', ''))
            result[i]         = project_title_err['Invalid-Maximum-Of-Length']
        

        # -------------------------------------------------------------------------------------------------------
        # validate that project description is set an is not empty
        if not 'project-description' in args or validation.validation_isEmpty(args['project-description']) or 'project-description' == None:
            i                   = i+1
            project_description = (error_handling_form.formError_invalidLength('#Project-Description', '', '', 'Please a Project-Description!'))
            result[i]           = project_description['Invalid-Empty-String']

        # validate that project description contains letters only
        elif validation.validation_isAlphaWithSpaces(args['project-description']) == False:
            i                   = i+1
            project_description = (error_handling_form.formError_invalidTypeError('#Project-Description', 'Project-Description', '', 'letters from a-z or A-Z! Spaces are not allowed'))
            result[i]           = project_description['Invalid-Arguments']
        
        # validate that project description has at least 2 Charactes
        elif validation.validation_minLength(args['project-description'], 15) == False:
            i                   = i+1
            project_description = (error_handling_form.formError_invalidLength('#Project-Description', '15', 'Project-Description', ''))
            result[i]           = project_description['Invalid-Minimum-Of-Length']
        
        
        # -------------------------------------------------------------------------------------------------------
         # validate that project description is set an is not empty
        if not 'project-end-date' in args or validation.validation_isEmpty(args['project-end-date']) or 'project-end-date' == None:
            i                   = i+1
            project_description = (error_handling_form.formError_invalidLength('#Project-End-Date', '', '', 'Please a Project-Enddate!'))
            result[i]           = project_description['Invalid-Empty-String']


        # -------------------------------------------------------------------------------------------------------
        # validate that no error was set during the above validating process -> if i = 1 -> no errors occured
        if i == 1:
            user_id    = args['user-id']
            # user_id    = 1
            project    = Project()
            tmp_result = project.project_createProject(user_id, args)


            if tmp_result:
                result[1]['status']                   = True
                result[1]['status-code']              = 200
                result[1]['status-description']       = 'OK'
                result[1]['redirect-status']          = True
                result[1]['redirect-target']          = 'http://127.0.0.1:5000/dashboard'
                result[1]['display-messages']         = None
                result[1]['display-messages-target '] = None


                return jsonify({
                    'status'          : result[1],
                    'count-result-set': project.NumResult,
                    'result-set-data' : project.Result
                })


            else:
                error_handling_db                     = DbError()
                result[1]['status']                   = False
                result[1]['status-code']              = 404
                result[1]['status-description']       = 'Error'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = None
                result[1]['display-messages']         = False
                result[1]['display-messages-target '] = None


                 # error handling in case no results were found
                if project.Error == '1':
                    tmp_error = (error_handling_db.dbError_noResultFound('#Project-Feedback'))
                    result[2] = tmp_error['No-Result-Found']
                    return result
                    
                # error handling in case email is already existing
                elif project.Error == '2':
                    tmp_error = (error_handling_db.dbError_IntegrityError('#Project-Feedback'))
                    result[2] = tmp_error['Multiple-Records-Found']
                    return result

                # error handling in case of an compile error
                elif project.Error == '3':
                    tmp_error = (error_handling_db.dbError_CompileError('#Project-Feedback'))
                    result[2] = tmp_error['Compile-Error']
                    return result

                # error handling in case of a DBAPI error
                elif project.Error == '4':
                    tmp_error = (error_handling_db.dbError_DBAPIError('#Project-Feedback'))
                    result[2] = tmp_error['DBAPI-Error']
                    return result
                    
                # error handling in case of some other internal errors or problems
                elif project.Error == '5':
                    tmp_error = (error_handling_db.dbError_InternalError('#Project-Feedback'))
                    result[2] = tmp_error['Internal-Error']
                    return result
                    
                # error handling in case that more than one result were found
                elif project.Error == '6':
                    tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Project-Feedback'))
                    result[2] = tmp_error['Multi-Records-Found']
                    return result
                    
                # error handling in case of an missing reference table error
                elif project.Error == '7':
                    tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Project-Feedback'))
                    result[2] = tmp_error['No-Referenced-Table']
                    return result
                    
                # error handling in case that object is not executable
                elif project.Error == '8':
                    tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Project-Feedback'))
                    result[2] = tmp_error['Object-Not-Executable']
                    return result
                    
                # error handling in case of other sqlalchmey errors
                elif project.Error == '9':
                    tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Project-Feedback'))
                    result[2] = tmp_error['SQL-Alchemy-Error']
                    return result
        return result




# --------------------------------------------------------------------------------------
# API Interface to update an existing project that belongs to the user loged in
# --------------------------------------------------------------------------------------
@api.route('/update-project', methods=['PUT'])
def api_updateProject():
    """
    This method is used to 

    Returns:
        [type]: [description]
    """

    method = request.method
    args   = request.args

    if method == 'PUT':
        i                   = 1
        validation          = Validation()
        error_handling_form = FormError()
        result              = {}
        result[1]           = {
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }
        
        # -------------------------------------------------------------------------------------------------------
        # validate that user-id is set and is not empty
        if not 'user-id' in args or validation.validation_isEmpty(args['user-id']) or 'user-id' == None:
            i           = i+1
            user_id_err = (error_handling_form.formError_invalidLength('#Project-Feedback', '', '', 'Please validate that an user is logged in to identify user project!'))
            result[i]   = user_id_err['Invalid-Empty-String']

        # -------------------------------------------------------------------------------------------------------
        # validate that project-id is set and is not empty
        if not 'project-id' in args or validation.validation_isEmpty(args['project-id']) or 'project-id' == None:
            i              = i+1
            project_id_err = (error_handling_form.formError_invalidLength('#Project-Feedback','', '', 'Please validate that an Project Id is set to identify the required project!'))
            result[i]      = project_id_err['Invalid-Empty-String']

        # -------------------------------------------------------------------------------------------------------
        # validate that project title is set and is not empty
        if not 'project-title' in args or validation.validation_isEmpty(args['project-title']) or 'project-title' == None:
            i                 = i+1
            project_title_err = (error_handling_form.formError_invalidLength('#Project-Title','', '', 'Please enter a Project Title!'))
            result[i]         = project_title_err['Invalid-Empty-String']

        # validate that project title contains letters only
        elif validation.validation_isAlphaWithSpaces(args['project-title']) == False:
            i                 = i+1
            project_title_err = (error_handling_form.formError_invalidTypeError('#Project-Title', 'Project Title', '', 'letters from a-z or A-Z! Spaces are not allowed'))
            result[i]         = project_title_err['Invalid-Arguments']

        # validate that project title has at least 2 Charactes
        elif validation.validation_minLength(args['project-title'], 2) == False:
            i                 = i+1
            project_title_err = (error_handling_form.formError_invalidLength('#Project-Title', '2', 'Project Title', ''))
            result[i]         = project_title_err['Invalid-Minimum-Of-Length'] 
            
        # validate that project title has not than more 75 Charactes
        elif validation.validation_maxLength(args['project-title'], 75) == False:
            i                 = i+1
            project_title_err = (error_handling_form.formError_invalidLength('#Project-Title', '75', 'Project Title', ''))
            result[i]         = project_title_err['Invalid-Maximum-Of-Length']
        
        # -------------------------------------------------------------------------------------------------------
        # validate that project description is set an is not empty
        if not 'project-description' in args or validation.validation_isEmpty(args['project-description']) or 'project-description' == None:
            i                   = i+1
            project_description = (error_handling_form.formError_invalidLength('#Project-Description', '', '', 'Please a Project-Description!'))
            result[i]           = project_description['Invalid-Empty-String']

        # validate that project description contains letters only
        elif validation.validation_isAlphaWithSpaces(args['project-description']) == False:
            i                   = i+1
            project_description = (error_handling_form.formError_invalidTypeError('#Project-Description', 'Project-Description', '', 'letters from a-z or A-Z! Spaces are not allowed'))
            result[i]           = project_description['Invalid-Arguments']
        
        # validate that project description has at least 2 Charactes
        elif validation.validation_minLength(args['project-description'], 15) == False:
            i                   = i+1
            project_description = (error_handling_form.formError_invalidLength('#Project-Description', '15', 'Project-Description', ''))
            result[i]           = project_description['Invalid-Minimum-Of-Length']
           
        # -------------------------------------------------------------------------------------------------------
        # validate that project description is set an is not empty
        if not 'project-end-date' in args or validation.validation_isEmpty(args['project-end-date']) or 'project-end-date' == None:
            i                   = i+1
            project_description = (error_handling_form.formError_invalidLength('#Project-End-Date', '', '', 'Please a Project-Enddate!'))
            result[i]           = project_description['Invalid-Empty-String']

        # -------------------------------------------------------------------------------------------------------
        # validate that no error was set during the above validating process -> if i = 1 -> no errors occured
        
        if i == 1:
            user_id    = args['user-id']

            project    = Project()
            tmp_result = project.project_updateProjectbyProjectId(user_id, args)


            if tmp_result:
                result[1]['status']                   = True
                result[1]['status-code']              = 200
                result[1]['status-description']       = 'OK'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = 'http://127.0.0.1:5000/dashboard'
                result[1]['display-messages']         = None
                result[1]['display-messages-target '] = None
                print(project.Result)
                return jsonify({
                    'status'          : result[1],
                    'count-result-set': project.NumResult,
                    'result-set-data' : project.Result
                })

            else:
                error_handling_db                     = DbError()
                result[1]['status']                   = False
                result[1]['status-code']              = 404
                result[1]['status-description']       = 'Error'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = None
                result[1]['display-messages']         = False
                result[1]['display-messages-target '] = None


                 # error handling in case no results were found
                if project.Error == '1':
                    tmp_error = (error_handling_db.dbError_noResultFound('#Project-Feedback'))
                    result[2] = tmp_error['No-Result-Found']
                    return result
                    
                # error handling in case email is already existing
                elif project.Error == '2':
                    tmp_error = (error_handling_db.dbError_IntegrityError('#Project-Feedback'))
                    result[2] = tmp_error['Multiple-Records-Found']
                    return result

                # error handling in case of an compile error
                elif project.Error == '3':
                    tmp_error = (error_handling_db.dbError_CompileError('#Project-Feedback'))
                    result[2] = tmp_error['Compile-Error']
                    return result

                # error handling in case of a DBAPI error
                elif project.Error == '4':
                    tmp_error = (error_handling_db.dbError_DBAPIError('#Project-Feedback'))
                    result[2] = tmp_error['DBAPI-Error']
                    return result
                    
                # error handling in case of some other internal errors or problems
                elif project.Error == '5':
                    tmp_error = (error_handling_db.dbError_InternalError('#Project-Feedback'))
                    result[2] = tmp_error['Internal-Error']
                    return result
                    
                # error handling in case that more than one result were found
                elif project.Error == '6':
                    tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Project-Feedback'))
                    result[2] = tmp_error['Multi-Records-Found']
                    return result
                    
                # error handling in case of an missing reference table error
                elif project.Error == '7':
                    tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Project-Feedback'))
                    result[2] = tmp_error['No-Referenced-Table']
                    return result
                    
                # error handling in case that object is not executable
                elif project.Error == '8':
                    tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Project-Feedback'))
                    result[2] = tmp_error['Object-Not-Executable']
                    return result
                    
                # error handling in case of other sqlalchmey errors
                elif project.Error == '9':
                    tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Project-Feedback'))
                    result[2] = tmp_error['SQL-Alchemy-Error']
                    return result
        return result
        



# --------------------------------------------------------------------------------------
# API Interface to delete an existing project that belongs to the user loged in
# --------------------------------------------------------------------------------------
@api.route('/delete-project', methods=['DELETE'])
def api_deleteProject():
    """
    This method is used to 
    """


    method = request.method
    args   = request.args

    if method == 'DELETE':
        i                   = 1
        validation          = Validation()
        error_handling_form = FormError()
        result              = {}
        result[1]           = {
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }

        # -------------------------------------------------------------------------------------------------------
        # validate that user-id is set and is not empty
        if not 'user-id' in args or validation.validation_isEmpty(args['user-id']) or 'user-id' == None:
            i           = i+1
            user_id_err = (error_handling_form.formError_invalidLength('#Project-Feedback', '', '', 'Please validate that an user is logged in to be able to delete a specific user project!'))
            result[i]   = user_id_err['Invalid-Empty-String']
        # -------------------------------------------------------------------------------------------------------
        # validate that project-id is set and is not empty
        if not 'project-id' in args or validation.validation_isEmpty(args['project-id']) or 'project-id' == None:
            i              = i+1
            project_id_err = (error_handling_form.formError_invalidLength('#Project-Feedback','', '', 'Please validate that an Project Id is set to identify the required project that should be deleted!'))
            result[i]      = project_id_err['Invalid-Empty-String']

        # -------------------------------------------------------------------------------------------------------
        # validate that no error was set during the above validating process -> if i = 1 -> no errors occured
        if i == 1:
            user_id    = args['user-id']
            project_id = args['project-id']

            project    = Project()
            tmp_result = project.project_deleteProjectByProjectId(user_id, project_id)


            if tmp_result:
                result[1]['status']                   = True
                result[1]['status-code']              = 200
                result[1]['status-description']       = 'OK'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = 'http://127.0.0.1:5000/dashboard'
                result[1]['display-messages']         = None
                result[1]['display-messages-target '] = None

                return jsonify({
                    'status'          : result[1],
                    'count-result-set': project.NumResult,
                    'result-set-data' : project.Result
                })

            else:
                error_handling_db                     = DbError()
                result[1]['status']                   = False
                result[1]['status-code']              = 404
                result[1]['status-description']       = 'Error'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = None
                result[1]['display-messages']         = False
                result[1]['display-messages-target '] = None


                 # error handling in case no results were found
                if project.Error == '1':
                    tmp_error = (error_handling_db.dbError_noResultFound('#Project-Feedback'))
                    result[2] = tmp_error['No-Result-Found']
                    return result
                    
                # error handling in case email is already existing
                elif project.Error == '2':
                    tmp_error = (error_handling_db.dbError_IntegrityError('#Project-Feedback'))
                    result[2] = tmp_error['Multiple-Records-Found']
                    return result

                # error handling in case of an compile error
                elif project.Error == '3':
                    tmp_error = (error_handling_db.dbError_CompileError('#Project-Feedback'))
                    result[2] = tmp_error['Compile-Error']
                    return result

                # error handling in case of a DBAPI error
                elif project.Error == '4':
                    tmp_error = (error_handling_db.dbError_DBAPIError('#Project-Feedback'))
                    result[2] = tmp_error['DBAPI-Error']
                    return result
                    
                # error handling in case of some other internal errors or problems
                elif project.Error == '5':
                    tmp_error = (error_handling_db.dbError_InternalError('#Project-Feedback'))
                    result[2] = tmp_error['Internal-Error']
                    return result
                    
                # error handling in case that more than one result were found
                elif project.Error == '6':
                    tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Project-Feedback'))
                    result[2] = tmp_error['Multi-Records-Found']
                    return result
                    
                # error handling in case of an missing reference table error
                elif project.Error == '7':
                    tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Project-Feedback'))
                    result[2] = tmp_error['No-Referenced-Table']
                    return result
                    
                # error handling in case that object is not executable
                elif project.Error == '8':
                    tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Project-Feedback'))
                    result[2] = tmp_error['Object-Not-Executable']
                    return result
                    
                # error handling in case of other sqlalchmey errors
                elif project.Error == '9':
                    tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Project-Feedback'))
                    result[2] = tmp_error['SQL-Alchemy-Error']
                    return result
        return result





# --------------------------------------------------------------------------------------
# API Interface to get all existing projects
# --------------------------------------------------------------------------------------
@api.route('/get-all-tasks', methods=['GET'])
def api_getAllTasks():
    """
    This method is used to get all tasks that are stored in the database, convert them into a formated JSON object, and return it to the client, which sent the request to this API. During this process, errorhandling will also be established,
    in case of some database failure or errors.

    Args:
        * Contains or uses no Arguments

    Returns:
        * JSON object: This method will return a JSON object list with all tasks that are available in the databasetable tbl_task_list

    Tests:
        * test that databse connection can be established
        * test stability and performance if database contains a huge amout of tasks such as hundred thousands of tasks
    """
    method = request.method
    if method == 'GET':
        result              = {}
        result[1]           = {
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }            

        tasks = Task()
        tmp     = tasks.task_getAllTasks()                                          # If there was no DB Error when selecting Projects, the variable will be true
            
        if tmp:
            result [1]['status']                   = True
            result [1]['status-code']              = 200
            result [1]['status-description']       = 'OK'
            result [1]['redirect-status']          = True
            result [1]['redirect-target']          = 'http://127.0.0.1:5000/dashboard'
            result [1]['display-messages']         = None
            result [1]['display-messages-target '] = None

            
            return jsonify({
                'status'          : result[1],
                'count-result-set': tasks.NumResult,
                'result-set-data' : tasks.Result
            })

        else:
            error_handling_db                      = DbError()
            result [1]['status']                   = False
            result [1]['status-code']              = 404
            result [1]['status-description']       = 'Error'
            result [1]['redirect-status']          = False
            result [1]['redirect-target']          = None
            result [1]['display-messages']         = 'inpage-alert'
            result [1]['display-messages-target '] = '#Task-Feedback-Error-Wrapper'

            # error handling in case no results were found
            if tasks.Error == '1':
                tmp_error = (error_handling_db.dbError_noResultFound('#Task-Feedback'))
                result[3] = tmp_error['No-Result-Found']
                return result
                
            # error handling in case email is already existing
            elif tasks.Error == '2':
                tmp_error = (error_handling_db.dbError_IntegrityError('#Task-Feedback'))
                result[3] = tmp_error['Multiple-Records-Found']
                return result

            # error handling in case of an compile error
            elif tasks.Error == '3':
                tmp_error = (error_handling_db.dbError_CompileError('#Task-Feedback'))
                result[3] = tmp_error['Compile-Error']
                return result

            # error handling in case of a DBAPI error
            elif tasks.Error == '4':
                tmp_error = (error_handling_db.dbError_DBAPIError('#Task-Feedback'))
                result[3] = tmp_error['DBAPI-Error']
                return result
                
            # error handling in case some other internal errors or problems
            elif tasks.Error == '5':
                tmp_error = (error_handling_db.dbError_InternalError('#Task-Feedback'))
                result[3] = tmp_error['Internal-Error']
                return result
                
            # error handling in case that more than one result were found
            elif tasks.Error == '6':
                tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Task-Feedback'))
                result[3] = tmp_error['Multi-Records-Found']
                return result
                
            # error handling in case of an missing reference table error
            elif tasks.Error == '7':
                tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Task-Feedback'))
                result[3] = tmp_error['No-Referenced-Table']
                return result
                
            # error handling in case that object is not executable
            elif tasks.Error == '8':
                tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Task-Feedback'))
                result[3] = tmp_error['Object-Not-Executable']
                return result
                
            # error handling in case of other sqlalchmey errors
            elif tasks.Error == '9':
                tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Task-Feedback'))
                result[3] = tmp_error['SQL-Alchemy-Error']
                return result

        return result





@api.route('/get-all-tasks-by-user', methods=['GET'])
def api_getAllTasksByUser():
    """
    This method is used to get all tasks that belongs to a specific user and that are stored in the database table tbl_task_list, convert them into a formated JSON object, and return it to the client, which sent the request to this API.
    During this process, errorhandling will also be established in case of some database failure or errors.

    Args:
        * user-id (Integer): When sending a request to the api.rout(/get-all-tasks-by-user), a user id has to be send within the request, otherwise it is not possible to get only the tasks, that belongs to a specific user.

    Returns:
        * JSON object: This method will return a JSON object list, with all tasks that belongs to the spcific user, from which the user-id was given and are available in the databasetable tbl_task_list

    Test:
        * test what will happen, if an string or char is given with the request to identify the users project, instead of an interger
        * test what will happen if an user id is given with the request which does not exists in the user table tbl_user_list
    """

    method = request.method
    args   = request.args

    if method == 'GET':
        i                   = 1
        validation          = Validation()
        error_handling_form = FormError()
        result              = {}
        result[1]           = {
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }            

        # -------------------------------------------------------------------------------------------------------
        # validate that user-id is set and is not empty
        if not 'user-id' in args or validation.validation_isEmpty(args['user-id']) or 'user-id' == None:
            i           = i+1
            user_id_err = (error_handling_form.formError_invalidLength('#Task-Feedback', '', '', 'Please validate that an user is logged in to get user tasks!'))
            result[i]   = user_id_err['Invalid-Empty-String']
        # -------------------------------------------------------------------------------------------------------
        # validate that no error was set during the above validating process -> if i = 1 -> no errors occured
        if i == 1:
            user_id    = args['user-id']
            tasks      = Task()
            tmp_result = tasks.task_getAllTasksByUsername(user_id)


            if tmp_result:
                result[1]['status']                   = True
                result[1]['status-code']              = 200
                result[1]['status-description']       = 'OK'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = 'http://127.0.0.1:5000/dashboard'
                result[1]['display-messages']         = None
                result[1]['display-messages-target '] = None

                return jsonify({
                    'status'          : result[1],
                    'count-result-set': tasks.NumResult,
                    'result-set-data' : tasks.Result
                })

            else:
                error_handling_db                     = DbError()
                result[1]['status']                   = False
                result[1]['status-code']              = 404
                result[1]['status-description']       = 'Error'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = None
                result[1]['display-messages']         = False
                result[1]['display-messages-target '] = None


                # error handling in case no results were found
                if tasks.Error == '1':
                    tmp_error = (error_handling_db.dbError_noResultFound('#Task-Feedback'))
                    result[2] = tmp_error['No-Result-Found']
                    return result
                    
                # error handling in case email is already existing
                elif tasks.Error == '2':
                    tmp_error = (error_handling_db.dbError_IntegrityError('#Task-Feedback'))
                    result[2] = tmp_error['Multiple-Records-Found']
                    return result

                # error handling in case of an compile error
                elif tasks.Error == '3':
                    tmp_error = (error_handling_db.dbError_CompileError('#Task-Feedback'))
                    result[2] = tmp_error['Compile-Error']
                    return result

                # error handling in case of a DBAPI error
                elif tasks.Error == '4':
                    tmp_error = (error_handling_db.dbError_DBAPIError('#Task-Feedback'))
                    result[2] = tmp_error['DBAPI-Error']
                    return result
                    
                # error handling in case of some other internal errors or problems
                elif tasks.Error == '5':
                    tmp_error = (error_handling_db.dbError_InternalError('#Task-Feedback'))
                    result[2] = tmp_error['Internal-Error']
                    return result
                    
                # error handling in case that more than one result were found
                elif tasks.Error == '6':
                    tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Task-Feedback'))
                    result[2] = tmp_error['Multi-Records-Found']
                    return result
                    
                # error handling in case of an missing reference table error
                elif tasks.Error == '7':
                    tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Task-Feedback'))
                    result[2] = tmp_error['No-Referenced-Table']
                    return result
                    
                # error handling in case that object is not executable
                elif tasks.Error == '8':
                    tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Task-Feedback'))
                    result[2] = tmp_error['Object-Not-Executable']
                    return result
                    
                # error handling in case of other sqlalchmey errors
                elif tasks.Error == '9':
                    tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Task-Feedback'))
                    result[2] = tmp_error['SQL-Alchemy-Error']
                    return result

        return result







@api.route('/get-all-tasks-by-username-group-by', methods=['GET'])
def api_getAllTaskByUsernameGroupBy():
    """
    This method is used to get all task that are grouped by a category and belongs to a specific user and which are stored in the database table tbl_task_list, convert them into a formated JSON object, and return it to the client, which sent the request to this API.
    During this process, errorhandling will also be established in case of some database failure or errors.

    Args:
        * user-id (Integer): When sending a request to the api.route(/get-all-task-by-username-group-by), a user id has to be send within the request, otherwise it is not possible to get only the tasks grouped by category, that belongs to a specific user.

    Returns:
        * JSON object: This method will return a JSON object list, with all tasks which are grouped by a category and belongs to the spcific user, from which the user-id was given and are available in the databasetable tbl_task_list

    Test:
        * test what will happen, if an string or char is given with the request to identify the users project, instead of an interger
        * test what will happen if an user id is given with the request which does not exists in the user table tbl_user_list
    """

    method = request.method
    args   = request.args

    if method == 'GET':
        i                   = 1
        validation          = Validation()
        error_handling_form = FormError()
        result              = {}
        result[1]           = {
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }            

        # -------------------------------------------------------------------------------------------------------
        # validate that user-id is set and is not empty
        if not 'user-id' in args or validation.validation_isEmpty(args['user-id']) or 'user-id' == None:
            i           = i+1
            user_id_err = (error_handling_form.formError_invalidLength('#Task-Feeback', '', '', 'Please validate that an user is logged in to get user tasks!'))
            result[i]   = user_id_err['Invalid-Empty-String']
            
        # -------------------------------------------------------------------------------------------------------
        # validate that category-id is set and is not empty
        if not 'project-id' in args or validation.validation_isEmpty(args['project-id']) or 'project-id' == None:
            i              = i+1
            project_id_err = (error_handling_form.formError_invalidLength('#Task-Feeback', '', '', 'Please validate that an porject-id is set to identify the required tasks!'))
            result[i]      = project_id_err['Invalid-Empty-String']
        # -------------------------------------------------------------------------------------------------------
        # validate that status-id is set and is not empty
        if not 'status-id' in args or validation.validation_isEmpty(args['status-id']) or 'status-id' == None:
            i             = i+1
            status_id_err = (error_handling_form.formError_invalidLength('#Task-Feeback', '', '', 'Please validate that an status-id is set to identify the required task by group!'))
            result[i]     = status_id_err['Invalid-Empty-String']
        # -------------------------------------------------------------------------------------------------------
        # validate that no error was set during the above validating process -> if i = 1 -> no errors occured
        if i == 1:
            user_id     = args['user-id']
            project_id  = args['project-id']
            category_id = args['status-id']
            tasks       = Task()
            tmp_result  = tasks.task_getAllTasksByUsernameGroup(user_id, project_id, category_id)


            if tmp_result:
                result[1]['status']                   = True
                result[1]['status-code']              = 200
                result[1]['status-description']       = 'OK'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = 'http://127.0.0.1:5000/dashboard'
                result[1]['display-messages']         = None
                result[1]['display-messages-target '] = None

                return jsonify({
                    'status'          : result[1],
                    'count-result-set': tasks.NumResult,
                    'result-set-data' : tasks.Result
                })

            else:
                error_handling_db                     = DbError()
                result[1]['status']                   = False
                result[1]['status-code']              = 404
                result[1]['status-description']       = 'Error'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = None
                result[1]['display-messages']         = False
                result[1]['display-messages-target '] = None


                # error handling in case no results were found
                if tasks.Error == '1':
                    tmp_error = (error_handling_db.dbError_noResultFound('#Project-Feedback'))
                    result[2] = tmp_error['No-Result-Found']
                    return result
                    
                # error handling in case email is already existing
                elif tasks.Error == '2':
                    tmp_error = (error_handling_db.dbError_IntegrityError('#Project-Feedback'))
                    result[2] = tmp_error['Multiple-Records-Found']
                    return result

                # error handling in case of an compile error
                elif tasks.Error == '3':
                    tmp_error = (error_handling_db.dbError_CompileError('#Project-Feedback'))
                    result[2] = tmp_error['Compile-Error']
                    return result

                # error handling in case of a DBAPI error
                elif tasks.Error == '4':
                    tmp_error = (error_handling_db.dbError_DBAPIError('#Project-Feedback'))
                    result[2] = tmp_error['DBAPI-Error']
                    return result
                    
                # error handling in case of some other internal errors or problems
                elif tasks.Error == '5':
                    tmp_error = (error_handling_db.dbError_InternalError('#Project-Feedback'))
                    result[2] = tmp_error['Internal-Error']
                    return result
                    
                # error handling in case that more than one result were found
                elif tasks.Error == '6':
                    tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Project-Feedback'))
                    result[2] = tmp_error['Multi-Records-Found']
                    return result
                    
                # error handling in case of an missing reference table error
                elif tasks.Error == '7':
                    tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Project-Feedback'))
                    result[2] = tmp_error['No-Referenced-Table']
                    return result
                    
                # error handling in case that object is not executable
                elif tasks.Error == '8':
                    tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Project-Feedback'))
                    result[2] = tmp_error['Object-Not-Executable']
                    return result
                    
                # error handling in case of other sqlalchmey errors
                elif tasks.Error == '9':
                    tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Project-Feedback'))
                    result[2] = tmp_error['SQL-Alchemy-Error']
                    return result

        return result







@api.route('/get-all-task-by-username-and-project', methods=['GET'])
def api_getAllTasksByUsernmaeProject():
    """
    This method is used to get all task that are grouped by a category and belongs to a specific user and which are stored in the database table tbl_task_list, convert them into a formated JSON object, and return it to the client, which sent the request to this API.
    During this process, errorhandling will also be established in case of some database failure or errors.

    Args:
        * user-id (Integer): When sending a request to the api.route(/get-all-task-by-username-group-by), a user id has to be send within the request, otherwise it is not possible to get only the tasks grouped by category, that belongs to a specific user.

    Returns:
        * JSON object: This method will return a JSON object list, with all tasks which are grouped by a category and belongs to the spcific user, from which the user-id was given and are available in the databasetable tbl_task_list

    Test:
        * test what will happen, if an string or char is given with the request to identify the users project, instead of an interger
        * test what will happen if an user id is given with the request which does not exists in the user table tbl_user_list
    """

    method = request.method
    args   = request.args

    if method == 'GET':
        i                   = 1
        validation          = Validation()
        error_handling_form = FormError()
        result              = {}
        result[1]           = {
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }            

        # -------------------------------------------------------------------------------------------------------
        # validate that user-id is set and is not empty
        if not 'user-id' in args or validation.validation_isEmpty(args['user-id']) or 'user-id' == None:
            i           = i+1
            user_id_err = (error_handling_form.formError_invalidLength('#Task-Feedback', '', '', 'Please validate that an user is logged in to get user tasks!'))
            result[i]   = user_id_err['Invalid-Empty-String']
            
        # -------------------------------------------------------------------------------------------------------
        # validate that category-id is set and is not empty
        if not 'project-id' in args or validation.validation_isEmpty(args['project-id']) or 'project-id' == None:
            i              = i+1
            project_id_err = (error_handling_form.formError_invalidLength('#Task-Feedback', '', '', 'Please validate that an porject-id is set to identify the required tasks!'))
            result[i]      = project_id_err['Invalid-Empty-String']
        # -------------------------------------------------------------------------------------------------------
        # validate that no error was set during the above validating process -> if i = 1 -> no errors occured
        if i == 1:
            user_id     = args['user-id']
            project_id  = args['project-id']
            tasks       = Task()
            tmp_result  = tasks.task_getAllTasksByUsernameProject(user_id, project_id)


            if tmp_result:
                result[1]['status']                   = True
                result[1]['status-code']              = 200
                result[1]['status-description']       = 'OK'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = 'http://127.0.0.1:5000/dashboard'
                result[1]['display-messages']         = None
                result[1]['display-messages-target '] = None

                return jsonify({
                    'status'          : result[1],
                    'count-result-set': tasks.NumResult,
                    'result-set-data' : tasks.Result
                })

            else:
                error_handling_db                     = DbError()
                result[1]['status']                   = False
                result[1]['status-code']              = 404
                result[1]['status-description']       = 'Error'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = None
                result[1]['display-messages']         = False
                result[1]['display-messages-target '] = None


                # error handling in case no results were found
                if tasks.Error == '1':
                    tmp_error = (error_handling_db.dbError_noResultFound('#Project-Feedback'))
                    result[2] = tmp_error['No-Result-Found']
                    return result
                    
                # error handling in case email is already existing
                elif tasks.Error == '2':
                    tmp_error = (error_handling_db.dbError_IntegrityError('#Project-Feedback'))
                    result[2] = tmp_error['Multiple-Records-Found']
                    return result

                # error handling in case of an compile error
                elif tasks.Error == '3':
                    tmp_error = (error_handling_db.dbError_CompileError('#Project-Feedback'))
                    result[2] = tmp_error['Compile-Error']
                    return result

                # error handling in case of a DBAPI error
                elif tasks.Error == '4':
                    tmp_error = (error_handling_db.dbError_DBAPIError('#Project-Feedback'))
                    result[2] = tmp_error['DBAPI-Error']
                    return result
                    
                # error handling in case of some other internal errors or problems
                elif tasks.Error == '5':
                    tmp_error = (error_handling_db.dbError_InternalError('#Project-Feedback'))
                    result[2] = tmp_error['Internal-Error']
                    return result
                    
                # error handling in case that more than one result were found
                elif tasks.Error == '6':
                    tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Project-Feedback'))
                    result[2] = tmp_error['Multi-Records-Found']
                    return result
                    
                # error handling in case of an missing reference table error
                elif tasks.Error == '7':
                    tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Project-Feedback'))
                    result[2] = tmp_error['No-Referenced-Table']
                    return result
                    
                # error handling in case that object is not executable
                elif tasks.Error == '8':
                    tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Project-Feedback'))
                    result[2] = tmp_error['Object-Not-Executable']
                    return result
                    
                # error handling in case of other sqlalchmey errors
                elif tasks.Error == '9':
                    tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Project-Feedback'))
                    result[2] = tmp_error['SQL-Alchemy-Error']
                    return result
        return result







@api.route('get-task-by-id', methods=['GET'])
def api_getTaskById():
    """
    This function is used to 

    Returns:
        [type]: [description]
    """

    method = request.method
    args   = request.args

    if method == 'GET':
        i                   = 1
        validation          = Validation()
        error_handling_form = FormError()
        result              = {}
        result[1]           = {
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }

        # -------------------------------------------------------------------------------------------------------
        # validate that user-id is set and is not empty
        if not 'user-id' in args or validation.validation_isEmpty(args['user-id']) or 'user-id' == None:
            i         = i+1
            user_id_err = (error_handling_form.formError_invalidLength('#Project-Feedback', '', '', 'Please validate that an user is logged in to get user projects!'))
            result[i]   = user_id_err['Invalid-Empty-String']
        # -------------------------------------------------------------------------------------------------------
        # validate that task-id is set and is not empty
        if not 'task-id' in args or validation.validation_isEmpty(args['task-id']) or 'task-id' == None:
            i           = i+1
            task_id_err = (error_handling_form.formError_invalidLength('#Task-Feedback','', '', 'Please validate that an Task Id is set to identify the required task!'))
            result[i]   = task_id_err['Invalid-Empty-String']

        # -------------------------------------------------------------------------------------------------------
        # validate that no error was set during the above validating process -> if i = 1 -> no errors occured
        if i == 1:
            user_id = args['user-id']
            task_id = args['task-id']

            task       = Task()
            tmp_result = task.task_getTaskById(user_id, task_id)


            if tmp_result:
                result[1]['status']                   = True
                result[1]['status-code']              = 200
                result[1]['status-description']       = 'OK'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = 'http://127.0.0.1:5000/dashboard'
                result[1]['display-messages']         = None
                result[1]['display-messages-target '] = None

                return jsonify({
                    'status'          : result[1],
                    'count-result-set': task.NumResult,
                    'result-set-data' : task.Result
                })

            else:
                error_handling_db                     = DbError()
                result[1]['status']                   = False
                result[1]['status-code']              = 404
                result[1]['status-description']       = 'Error'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = None
                result[1]['display-messages']         = False
                result[1]['display-messages-target '] = None


                 # error handling in case no results were found
                if task.Error == '1':
                    tmp_error = (error_handling_db.dbError_noResultFound('#Task-Feedback'))
                    result[2] = tmp_error['No-Result-Found']
                    return result
                    
                # error handling in case email is already existing
                elif task.Error == '2':
                    tmp_error = (error_handling_db.dbError_IntegrityError('#Task-Feedback'))
                    result[2] = tmp_error['Multiple-Records-Found']
                    return result

                # error handling in case of an compile error
                elif task.Error == '3':
                    tmp_error = (error_handling_db.dbError_CompileError('#Task-Feedback'))
                    result[2] = tmp_error['Compile-Error']
                    return result

                # error handling in case of a DBAPI error
                elif task.Error == '4':
                    tmp_error = (error_handling_db.dbError_DBAPIError('#Task-Feedback'))
                    result[2] = tmp_error['DBAPI-Error']
                    return result
                    
                # error handling in case of some other internal errors or problems
                elif task.Error == '5':
                    tmp_error = (error_handling_db.dbError_InternalError('#Task-Feedback'))
                    result[2] = tmp_error['Internal-Error']
                    return result
                    
                # error handling in case that more than one result were found
                elif task.Error == '6':
                    tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Task-Feedback'))
                    result[2] = tmp_error['Multi-Records-Found']
                    return result
                    
                # error handling in case of an missing reference table error
                elif task.Error == '7':
                    tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Task-Feedback'))
                    result[2] = tmp_error['No-Referenced-Table']
                    return result
                    
                # error handling in case that object is not executable
                elif task.Error == '8':
                    tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Task-Feedback'))
                    result[2] = tmp_error['Object-Not-Executable']
                    return result
                    
                # error handling in case of other sqlalchmey errors
                elif task.Error == '9':
                    tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Task-Feedback'))
                    result[2] = tmp_error['SQL-Alchemy-Error']
                    return result
        
        return result






@api.route('/create-task', methods=['POST'])
def api_createTask():
    """
    This function is used to create projects
    """
    method = request.method
    args   = request.form

    if method == 'POST':
        i                   = 1
        validation          = Validation()
        error_handling_form = FormError()
        result              = {}
        result[1]           = {
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }


        # -------------------------------------------------------------------------------------------------------
        # validate that user-id is set and is not empty
        if not 'user-id' in args or validation.validation_isEmpty(args['user-id']) or 'user-id' == None:
            i           = i+1
            user_id_err = (error_handling_form.formError_invalidLength('#Task-Feedback', '', '', 'Please validate that an user is logged in to get user tasks!'))
            result[i]   = user_id_err['Invalid-Empty-String']
            
        # -------------------------------------------------------------------------------------------------------
        # validate that category-id is set and is not empty
        if not 'project-id' in args or validation.validation_isEmpty(args['project-id']) or 'project-id' == None:
            i              = i+1
            project_id_err = (error_handling_form.formError_invalidLength('#Task-Feedback', '', '', 'Please validate that an porject-id is set to identify the required tasks!'))
            result[i]      = project_id_err['Invalid-Empty-String']

        # -------------------------------------------------------------------------------------------------------
        # validate that task title is set and is not empty
        if not 'task-title' in args or validation.validation_isEmpty(args['task-title']) or 'task-title' == None:
            i              = i+1
            task_title_err = (error_handling_form.formError_invalidLength('#Task-Title','', '', 'Please enter a Task Title!'))
            result[i]      = task_title_err['Invalid-Empty-String']

        # validate that task title contains letters only
        elif validation.validation_isAlphaWithSpaces(args['task-title']) == False:
            i              = i+1
            task_title_err = (error_handling_form.formError_invalidTypeError('#Task-Title', 'Task Title', '', 'letters from a-z or A-Z! Spaces are not allowed'))
            result[i]      = task_title_err['Invalid-Arguments']

        # validate that task title has at least 2 Charactes
        elif validation.validation_minLength(args['task-title'], 2) == False:
            i              = i+1
            task_title_err = (error_handling_form.formError_invalidLength('#Task-Title', '2', 'Task Title', ''))
            result[i]      = task_title_err['Invalid-Minimum-Of-Length'] 
            
        # validate that task title has not than more 75 Charactes
        elif validation.validation_maxLength(args['task-title'], 75) == False:
            i              = i+1
            task_title_err = (error_handling_form.formError_invalidLength('#Task-Title', '75', 'Task Title', ''))
            result[i]      = task_title_err['Invalid-Maximum-Of-Length']
        

        # -------------------------------------------------------------------------------------------------------
        # validate that task description is set an is not empty
        if not 'task-description' in args or validation.validation_isEmpty(args['task-description']) or 'task-description' == None:
            i                = i+1
            task_description = (error_handling_form.formError_invalidLength('#Task-Description', '', '', 'Please a Task-Description!'))
            result[i]        = task_description['Invalid-Empty-String']

        # validate that task description contains letters only
        elif validation.validation_isAlphaWithSpaces(args['task-description']) == False:
            i                = i+1
            task_description = (error_handling_form.formError_invalidTypeError('#Task-Description', 'Task-Description', '', 'letters from a-z or A-Z! Spaces are not allowed'))
            result[i]        = task_description['Invalid-Arguments']
        
        # validate that task description has at least 2 Charactes
        elif validation.validation_minLength(args['task-description'], 15) == False:
            i                = i+1
            task_description = (error_handling_form.formError_invalidLength('#Task-Description', '15', 'Task-Description', ''))
            result[i]        = task_description['Invalid-Minimum-Of-Length']
               
        # -------------------------------------------------------------------------------------------------------
        # validate that task status is set an is not empty
        if not 'task-status' in args or validation.validation_isEmpty(args['task-status']) or 'task-status' == None:
            i           = i+1
            task_status = (error_handling_form.formError_invalidLength('#Task-Status', '', '', 'Please a Task-Status!'))
            result[i]   = task_status['Invalid-Empty-String']

        # validate that task status contains letters only
        elif validation.validation_isAlpha(args['task-status']) == False:
            i           = i+1
            task_status = (error_handling_form.formError_invalidTypeError('#Task-Status', 'Task-Status', '', 'letters from a-z or A-Z! Spaces are not allowed'))
            result[i]   = task_status['Invalid-Arguments']
        
        # validate that task status has status done or in_progress or todo
        elif args['task-status'] != 'inprogress' and args['task-status'] != 'todo' and args['task-status'] != 'finished':
            i           = i+1
            task_status = (error_handling_form.formError_invalidTypeError('#Task-Status', 'Task-Status', '', 'In Progress, Todo or Done'))
            result[i]   = task_status['Invalid-Arguments']

        # -------------------------------------------------------------------------------------------------------
         # validate that task end date is set an is not empty
        if not 'task-end-date' in args or validation.validation_isEmpty(args['task-end-date']) or 'task-end-date' == None:
            i                 = i+1
            task_end_date_err = (error_handling_form.formError_invalidLength('#Task-End-Date', '', '', 'Please enter a Task-End-Date!'))
            result[i]         = task_end_date_err['Invalid-Empty-String']


        # -------------------------------------------------------------------------------------------------------
        # validate that no error was set during the above validating process -> if i = 1 -> no errors occured
        if i == 1:
            user_id    = args['user-id']
            project_id = args['project-id']
            # project_end_date = str(args['task-end-date'])
            # print(project_end_date)
            task       = Task()
            tmp_result = task.task_createTask(user_id, project_id, args)


            if tmp_result:
                result[1]['status']                   = True
                result[1]['status-code']              = 200
                result[1]['status-description']       = 'OK'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = "http://127.0.0.1:5000/dashboard/" 
                result[1]['display-messages']         = None
                result[1]['display-messages-target '] = None

                return jsonify({
                    'status'          : result[1],
                    'count-result-set': task.NumResult,
                    'result-set-data' : task.Result
                })

            else:
                error_handling_db                     = DbError()
                result[1]['status']                   = False
                result[1]['status-code']              = 404
                result[1]['status-description']       = 'Error'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = None
                result[1]['display-messages']         = False
                result[1]['display-messages-target '] = None


                 # error handling in case no results were found
                if task.Error == '1':
                    tmp_error = (error_handling_db.dbError_noResultFound('#Task-Feedback'))
                    result[2] = tmp_error['No-Result-Found']
                    return result
                    
                # error handling in case email is already existing
                elif task.Error == '2':
                    tmp_error = (error_handling_db.dbError_IntegrityError('#Task-Feedback'))
                    result[2] = tmp_error['Multiple-Records-Found']
                    return result

                # error handling in case of an compile error
                elif task.Error == '3':
                    tmp_error = (error_handling_db.dbError_CompileError('#Task-Feedback'))
                    result[2] = tmp_error['Compile-Error']
                    return result

                # error handling in case of a DBAPI error
                elif task.Error == '4':
                    tmp_error = (error_handling_db.dbError_DBAPIError('#Task-Feedback'))
                    result[2] = tmp_error['DBAPI-Error']
                    return result
                    
                # error handling in case of some other internal errors or problems
                elif task.Error == '5':
                    tmp_error = (error_handling_db.dbError_InternalError('#Task-Feedback'))
                    result[2] = tmp_error['Internal-Error']
                    return result
                    
                # error handling in case that more than one result were found
                elif task.Error == '6':
                    tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Task-Feedback'))
                    result[2] = tmp_error['Multi-Records-Found']
                    return result
                    
                # error handling in case of an missing reference table error
                elif task.Error == '7':
                    tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Task-Feedback'))
                    result[2] = tmp_error['No-Referenced-Table']
                    return result
                    
                # error handling in case that object is not executable
                elif task.Error == '8':
                    tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Task-Feedback'))
                    result[2] = tmp_error['Object-Not-Executable']
                    return result
                    
                # error handling in case of other sqlalchmey errors
                elif task.Error == '9':
                    tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Task-Feedback'))
                    result[2] = tmp_error['SQL-Alchemy-Error']
                    return result
        return result





@api.route('/update-task', methods=['PUT'])
def api_updateTask():
    """
    This method is used to 

    Returns:
        [type]: [description]
    """

    method = request.method
    args   = request.args

    if method == 'PUT':
        i                   = 1
        validation          = Validation()
        error_handling_form = FormError()
        result              = {}
        result[1]           = {
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }


        # -------------------------------------------------------------------------------------------------------
        # validate that user-id is set and is not empty
        if not 'user-id' in args or validation.validation_isEmpty(args['user-id']) or 'user-id' == None:
            i           = i+1
            user_id_err = (error_handling_form.formError_invalidLength('#Task-Feedback', '', '', 'Please validate that an user is logged in to identify user task!'))
            result[i]   = user_id_err['Invalid-Empty-String']

        # -------------------------------------------------------------------------------------------------------
        # validate that task-id is set and is not empty
        if not 'task-id' in args or validation.validation_isEmpty(args['task-id']) or 'task-id' == None:
            i           = i+1
            task_id_err = (error_handling_form.formError_invalidLength('#Task-Feedback','', '', 'Please validate that an Task Id is set to identify the required task!'))
            result[i]   = task_id_err['Invalid-Empty-String']

        # -------------------------------------------------------------------------------------------------------
        # validate that task title is set and is not empty
        if not 'task-title' in args or validation.validation_isEmpty(args['task-title']) or 'task-title' == None:
            i              = i+1
            task_title_err = (error_handling_form.formError_invalidLength('#Task-Title','', '', 'Please enter a Task Title!'))
            result[i]      = task_title_err['Invalid-Empty-String']

        # validate that task title contains letters only
        elif validation.validation_isAlpha(args['task-title']) == False:
            i              = i+1
            task_title_err = (error_handling_form.formError_invalidTypeError('#Task-Title', 'Task Title', '', 'letters from a-z or A-Z! Spaces are not allowed'))
            result[i]      = task_title_err['Invalid-Arguments']

        # validate that tasl title has at least 2 Charactes
        elif validation.validation_minLength(args['task-title'], 2) == False:
            i              = i+1
            task_title_err = (error_handling_form.formError_invalidLength('#Task-Title', '2', 'Task Title', ''))
            result[i]      = task_title_err['Invalid-Minimum-Of-Length'] 
            
        # validate that task title has not than more 75 Charactes
        elif validation.validation_maxLength(args['task-title'], 75) == False:
            i              = i+1
            task_title_err = (error_handling_form.formError_invalidLength('#Task-Title', '75', 'Task Title', ''))
            result[i]      = task_title_err['Invalid-Maximum-Of-Length']
        
        # -------------------------------------------------------------------------------------------------------
        # validate that task description is set an is not empty
        if not 'task-description' in args or validation.validation_isEmpty(args['task-description']) or 'task-description' == None:
            i                = i+1
            task_description = (error_handling_form.formError_invalidLength('#Task-Description', '', '', 'Please a Task-Description!'))
            result[i]        = task_description['Invalid-Empty-String']

        # validate that task description contains letters only
        elif validation.validation_isAlpha(args['task-description']) == False:
            i                = i+1
            task_description = (error_handling_form.formError_invalidTypeError('#Task-Description', 'Task-Description', '', 'letters from a-z or A-Z! Spaces are not allowed'))
            result[i]        = task_description['Invalid-Arguments']
        
        # validate that task description has at least 2 Charactes
        elif validation.validation_minLength(args['task-description'], 15) == False:
            i                = i+1
            task_description = (error_handling_form.formError_invalidLength('#Task-Description', '15', 'Task-Description', ''))
            result[i]        = task_description['Invalid-Minimum-Of-Length']
           
        # -------------------------------------------------------------------------------------------------------
        # validate that task status is set an is not empty
        if not 'task-status' in args or validation.validation_isEmpty(args['task-status']) or 'task-status' == None:
            i           = i+1
            task_status = (error_handling_form.formError_invalidLength('#Task-Status', '', '', 'Please a Task-Status!'))
            result[i]   = task_status['Invalid-Empty-String']

        # validate that task status contains letters only
        elif validation.validation_isAlpha(args['task-status']) == False:
            i           = i+1
            task_status = (error_handling_form.formError_invalidTypeError('#Task-Status', 'Task-Status', '', 'letters from a-z or A-Z! Spaces are not allowed'))
            result[i]   = task_status['Invalid-Arguments']
        
        # validate that task status has status done or in_progress or todo
        elif args['task-status'] != 'inprogress' and args['task-status'] != 'todo' and args['task-status'] != 'finished':
            i           = i+1
            task_status = (error_handling_form.formError_invalidTypeError('#Task-Status', 'Task-Status', '', 'In Progress, Todo or Done'))
            result[i]   = task_status['Invalid-Arguments']
        
        # -------------------------------------------------------------------------------------------------------
        # validate that task description is set an is not empty
        if not 'task-end-date' in args or validation.validation_isEmpty(args['task-end-date']) or 'task-end-date' == None:
            i                = i+1
            task_description = (error_handling_form.formError_invalidLength('#Task-End-Date', '', '', 'Please a Task-Enddate!'))
            result[i]        = task_description['Invalid-Empty-String']

        # -------------------------------------------------------------------------------------------------------
        # validate that no error was set during the above validating process -> if i = 1 -> no errors occured
        if i == 1:
            user_id    = args['user-id']
            task_id    = args['task-id']

            task       = Task()
            tmp_result = task.task_updateTaskById(user_id, task_id, args)


            if tmp_result:
                result[1]['status']                   = True
                result[1]['status-code']              = 200
                result[1]['status-description']       = 'OK'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = 'http://127.0.0.1:5000/dashboard'
                result[1]['display-messages']         = None
                result[1]['display-messages-target '] = None

                return jsonify({
                    'status'          : result[1],
                    'count-result-set': task.NumResult,
                    'result-set-data' : task.Result
                })

            else:
                error_handling_db                     = DbError()
                result[1]['status']                   = False
                result[1]['status-code']              = 404
                result[1]['status-description']       = 'Error'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = None
                result[1]['display-messages']         = False
                result[1]['display-messages-target '] = None


                 # error handling in case no results were found
                if task.Error == '1':
                    tmp_error = (error_handling_db.dbError_noResultFound('#Task-Feedback'))
                    result[2] = tmp_error['No-Result-Found']
                    return result
                    
                # error handling in case email is already existing
                elif task.Error == '2':
                    tmp_error = (error_handling_db.dbError_IntegrityError('#Task-Feedback'))
                    result[2] = tmp_error['Multiple-Records-Found']
                    return result

                # error handling in case of an compile error
                elif task.Error == '3':
                    tmp_error = (error_handling_db.dbError_CompileError('#Task-Feedback'))
                    result[2] = tmp_error['Compile-Error']
                    return result

                # error handling in case of a DBAPI error
                elif task.Error == '4':
                    tmp_error = (error_handling_db.dbError_DBAPIError('#Task-Feedback'))
                    result[2] = tmp_error['DBAPI-Error']
                    return result
                    
                # error handling in case of some other internal errors or problems
                elif task.Error == '5':
                    tmp_error = (error_handling_db.dbError_InternalError('#Task-Feedback'))
                    result[2] = tmp_error['Internal-Error']
                    return result
                    
                # error handling in case that more than one result were found
                elif task.Error == '6':
                    tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Task-Feedback'))
                    result[2] = tmp_error['Multi-Records-Found']
                    return result
                    
                # error handling in case of an missing reference table error
                elif task.Error == '7':
                    tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Task-Feedback'))
                    result[2] = tmp_error['No-Referenced-Table']
                    return result
                    
                # error handling in case that object is not executable
                elif task.Error == '8':
                    tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Task-Feedback'))
                    result[2] = tmp_error['Object-Not-Executable']
                    return result
                    
                # error handling in case of other sqlalchmey errors
                elif task.Error == '9':
                    tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Task-Feedback'))
                    result[2] = tmp_error['SQL-Alchemy-Error']
                    return result
        
        return result





@api.route('/update-task-status', methods=['PUT'])
def api_updateTaskStatus():
    """
    This method is used to 

    Returns:
        [type]: [description]
    """

    method = request.method
    args   = request.args

    if method == 'PUT':
        i                   = 1
        validation          = Validation()
        error_handling_form = FormError()
        result              = {}
        result[1]           = {
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }


        # -------------------------------------------------------------------------------------------------------
        # validate that user-id is set and is not empty
        if not 'user-id' in args or validation.validation_isEmpty(args['user-id']) or 'user-id' == None:
            i           = i+1
            user_id_err = (error_handling_form.formError_invalidLength('#Task-Feedback', '', '', 'Please validate that an user is logged in to identify user task!'))
            result[i]   = user_id_err['Invalid-Empty-String']

        # -------------------------------------------------------------------------------------------------------
        # validate that task-id is set and is not empty
        if not 'task-id' in args or validation.validation_isEmpty(args['task-id']) or 'task-id' == None:
            i           = i+1
            task_id_err = (error_handling_form.formError_invalidLength('#Task-Feedback','', '', 'Please validate that an Task Id is set to identify the required task!'))
            result[i]   = task_id_err['Invalid-Empty-String']

        # -------------------------------------------------------------------------------------------------------
        # validate that task status is set an is not empty
        if not 'task-status' in args or validation.validation_isEmpty(args['task-status']) or 'task-status' == None:
            i           = i+1
            task_status = (error_handling_form.formError_invalidLength('#Task-Status', '', '', 'Please a Task-Status!'))
            result[i]   = task_status['Invalid-Empty-String']

        # validate that task status contains letters only
        elif validation.validation_isAlpha(args['task-status']) == False:
            i           = i+1
            task_status = (error_handling_form.formError_invalidTypeError('#Task-Status', 'Task-Status', '', 'letters from a-z or A-Z! Spaces are not allowed'))
            result[i]   = task_status['Invalid-Arguments']
        
        # validate that task status has status done or in_progress or todo
        elif args['task-status'] != 'inprogress' and args['task-status'] != 'todo' and args['task-status'] != 'finished':
            i           = i+1
            task_status = (error_handling_form.formError_invalidTypeError('#Task-Status', 'Task-Status', '', 'In Progress, Todo or Done'))
            result[i]   = task_status['Invalid-Arguments']
           
        # -------------------------------------------------------------------------------------------------------
        # validate that no error was set during the above validating process -> if i = 1 -> no errors occured
        if i == 1:
            user_id    = args['user-id']
            task_id    = args['task-id']

            task       = Task()
            tmp_result = task.task_updateTaskStatusById(user_id, task_id, args)


            if tmp_result:
                result[1]['status']                   = True
                result[1]['status-code']              = 200
                result[1]['status-description']       = 'OK'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = 'http://127.0.0.1:5000/dashboard'
                result[1]['display-messages']         = None
                result[1]['display-messages-target '] = None

                return jsonify({
                    'status'          : result[1],
                    'count-result-set': task.NumResult,
                    'result-set-data' : task.Result
                })

            else:
                error_handling_db                     = DbError()
                result[1]['status']                   = False
                result[1]['status-code']              = 404
                result[1]['status-description']       = 'Error'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = None
                result[1]['display-messages']         = False
                result[1]['display-messages-target '] = None


                 # error handling in case no results were found
                if task.Error == '1':
                    tmp_error = (error_handling_db.dbError_noResultFound('#Task-Feedback'))
                    result[2] = tmp_error['No-Result-Found']
                    return result
                    
                # error handling in case email is already existing
                elif task.Error == '2':
                    tmp_error = (error_handling_db.dbError_IntegrityError('#Task-Feedback'))
                    result[2] = tmp_error['Multiple-Records-Found']
                    return result

                # error handling in case of an compile error
                elif task.Error == '3':
                    tmp_error = (error_handling_db.dbError_CompileError('#Task-Feedback'))
                    result[2] = tmp_error['Compile-Error']
                    return result

                # error handling in case of a DBAPI error
                elif task.Error == '4':
                    tmp_error = (error_handling_db.dbError_DBAPIError('#Task-Feedback'))
                    result[2] = tmp_error['DBAPI-Error']
                    return result
                    
                # error handling in case of some other internal errors or problems
                elif task.Error == '5':
                    tmp_error = (error_handling_db.dbError_InternalError('#Task-Feedback'))
                    result[2] = tmp_error['Internal-Error']
                    return result
                    
                # error handling in case that more than one result were found
                elif task.Error == '6':
                    tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Task-Feedback'))
                    result[2] = tmp_error['Multi-Records-Found']
                    return result
                    
                # error handling in case of an missing reference table error
                elif task.Error == '7':
                    tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Task-Feedback'))
                    result[2] = tmp_error['No-Referenced-Table']
                    return result
                    
                # error handling in case that object is not executable
                elif task.Error == '8':
                    tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Task-Feedback'))
                    result[2] = tmp_error['Object-Not-Executable']
                    return result
                    
                # error handling in case of other sqlalchmey errors
                elif task.Error == '9':
                    tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Task-Feedback'))
                    result[2] = tmp_error['SQL-Alchemy-Error']
                    return result
        
        return result





@api.route('/delete-task-by-id', methods=['DELETE'])
def api_deleteTaskById():
    """
    This method is used to 
    """


    method = request.method
    args   = request.args

    if method == 'DELETE':
        i                   = 1
        validation          = Validation()
        error_handling_form = FormError()
        result              = {}
        result[1]           = {
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }

        # -------------------------------------------------------------------------------------------------------
        # validate that user-id is set and is not empty
        if not 'user-id' in args or validation.validation_isEmpty(args['user-id']) or 'user-id' == None:
            i           = i+1
            user_id_err = (error_handling_form.formError_invalidLength('#Task-Feedback', '', '', 'Please validate that an user is logged in to be able to delete a specific user Task!'))
            result[i]   = user_id_err['Invalid-Empty-String']
        # -------------------------------------------------------------------------------------------------------
        # validate that project-id is set and is not empty
        if not 'task-id' in args or validation.validation_isEmpty(args['task-id']) or 'task-id' == None:
            i           = i+1
            task_id_err = (error_handling_form.formError_invalidLength('#Task-Feedback','', '', 'Please validate that an Task Id is set to identify the required Task that should be deleted!'))
            result[i]   = task_id_err['Invalid-Empty-String']

        # -------------------------------------------------------------------------------------------------------
        # validate that no error was set during the above validating process -> if i = 1 -> no errors occured
        if i == 1:
            user_id    = args['user-id']
            task_id    = args['task-id']

            task       = Task()
            tmp_result = task.task_deleteTaskById(user_id, task_id)


            if tmp_result:
                result[1]['status']                   = True
                result[1]['status-code']              = 200
                result[1]['status-description']       = 'OK'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = 'http://127.0.0.1:5000/dashboard'
                result[1]['display-messages']         = None
                result[1]['display-messages-target '] = None

                return jsonify({
                    'status'          : result[1],
                    'count-result-set': task.NumResult,
                    'result-set-data' : task.Result
                })

            else:
                error_handling_db                     = DbError()
                result[1]['status']                   = False
                result[1]['status-code']              = 404
                result[1]['status-description']       = 'Error'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = None
                result[1]['display-messages']         = False
                result[1]['display-messages-target '] = None


                 # error handling in case no results were found
                if task.Error == '1':
                    tmp_error = (error_handling_db.dbError_noResultFound('#Task-Feedback'))
                    result[2] = tmp_error['No-Result-Found']
                    return result
                    
                # error handling in case email is already existing
                elif task.Error == '2':
                    tmp_error = (error_handling_db.dbError_IntegrityError('#Task-Feedback'))
                    result[2] = tmp_error['Multiple-Records-Found']
                    return result

                # error handling in case of an compile error
                elif task.Error == '3':
                    tmp_error = (error_handling_db.dbError_CompileError('#Task-Feedback'))
                    result[2] = tmp_error['Compile-Error']
                    return result

                # error handling in case of a DBAPI error
                elif task.Error == '4':
                    tmp_error = (error_handling_db.dbError_DBAPIError('#Task-Feedback'))
                    result[2] = tmp_error['DBAPI-Error']
                    return result
                    
                # error handling in case of some other internal errors or problems
                elif task.Error == '5':
                    tmp_error = (error_handling_db.dbError_InternalError('#Task-Feedback'))
                    result[2] = tmp_error['Internal-Error']
                    return result
                    
                # error handling in case that more than one result were found
                elif task.Error == '6':
                    tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Task-Feedback'))
                    result[2] = tmp_error['Multi-Records-Found']
                    return result
                    
                # error handling in case of an missing reference table error
                elif task.Error == '7':
                    tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Task-Feedback'))
                    result[2] = tmp_error['No-Referenced-Table']
                    return result
                    
                # error handling in case that object is not executable
                elif task.Error == '8':
                    tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Task-Feedback'))
                    result[2] = tmp_error['Object-Not-Executable']
                    return result
                    
                # error handling in case of other sqlalchmey errors
                elif task.Error == '9':
                    tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Task-Feedback'))
                    result[2] = tmp_error['SQL-Alchemy-Error']
                    return result

        return result




@api.route('/get-number-of-tasks-where-status-is', methods=['GET'])
def api_getNumberOfTasksWhereStatusFinished():
    """
    This method is used to get a number of all tasks that have the status 'finished' and belongs to a specific user and which are stored in the database table tbl_task_list, convert them into a formated JSON object, and return it to the client, which sent the request to this API.
    During this process, errorhandling will also be established in case of some database failure or errors.

    Args:
        * user-id (Integer): When sending a request to the api.route(/get-all-task-by-username-group-by), a user id has to be send within the request, otherwise it is not possible to get only the tasks grouped by category, that belongs to a specific user.

    Returns:
        * JSON object: This method will return a JSON object list, with all tasks which are grouped by a category and belongs to the spcific user, from which the user-id was given and are available in the databasetable tbl_task_list

    Test:
        * test what will happen, if an string or char is given with the request to identify the users project, instead of an interger
        * test what will happen if an user id is given with the request which does not exists in the user table tbl_user_list
    """

    method = request.method
    args   = request.args

    if method == 'GET':
        i                   = 1
        validation          = Validation()
        error_handling_form = FormError()
        result              = {}
        result[1]           = {
            'status'                 : False,                                       # False if an error occured, True if everything went as planned
            'status-code'            : None,                                        # Contains an status code
            'status-description'     : None,                                        # contains a description about the current status
            'redirect-status'        : False,                                       # true when use will be redirected to another page when function was successfully executed, false if user should stay on the same page
            'redirect-target'        : None,                                        # Contains the URL where user will be redirected if redirection is enabled (true)
            'display-messages'       : None,                                        # Contains information about if the message should appear on the same webpage or on another one where it will be flashed
            'display-messages-target': None                                         # Contains the HTML Id from the wrapper div-box where the message will be displayed
        }            

        # -------------------------------------------------------------------------------------------------------
        # validate that user-id is set and is not empty
        if not 'user-id' in args or validation.validation_isEmpty(args['user-id']) or 'user-id' == None:
            i           = i+1
            user_id_err = (error_handling_form.formError_invalidLength('#Task-Feedback', '', '', 'Please validate that an user is logged in to get number of user tasks with specific category!'))
            result[i]   = user_id_err['Invalid-Empty-String']
            
        # -------------------------------------------------------------------------------------------------------
        # validate that category-id is set and is not empty
        if not 'category-id' in args or validation.validation_isEmpty(args['category-id']) or 'category-id' == None:
            i               = i+1
            category_id_err = (error_handling_form.formError_invalidLength('#Task-Feedback', '', '', 'Please validate that an category-id is set to identify the required task by group!'))
            result[i]       = category_id_err['Invalid-Empty-String']

        # -------------------------------------------------------------------------------------------------------
        # validate that no error was set during the above validating process -> if i = 1 -> no errors occured
        if i == 1:
            
            # -------------------------------------------------------------------------------------------------------
            # Validate that project id is set to group result by projects if not set the total number of tasks of user will be returened
            if 'project-id' in args and validation.validation_isEmpty(args['category-id']) == False and 'project-id' != None:
                project_id = args['project-id'] 
            else:
                project_id = None

            user_id     = args['user-id']
            category_id = args['category-id']
            tasks       = Task()
            tmp_result  = tasks.task_getNumberofTasksWhereStatus(user_id, category_id, project_id)


            if tmp_result:
                result[1]['status']                   = True
                result[1]['status-code']              = 200
                result[1]['status-description']       = 'OK'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = 'http://127.0.0.1:5000/dashboard'
                result[1]['display-messages']         = None
                result[1]['display-messages-target '] = None

                return jsonify({
                    'status'          : result[1],
                    'count-result-set': tasks.NumResult,
                    'result-set-data' : tasks.Result
                })

            else:
                error_handling_db                     = DbError()
                result[1]['status']                   = False
                result[1]['status-code']              = 404
                result[1]['status-description']       = 'Error'
                result[1]['redirect-status']          = False
                result[1]['redirect-target']          = None
                result[1]['display-messages']         = False
                result[1]['display-messages-target '] = None


                # error handling in case no results were found
                if tasks.Error == '1':
                    tmp_error = (error_handling_db.dbError_noResultFound('#Task-Feedback'))
                    result[2] = tmp_error['No-Result-Found']
                    return result
                    
                # error handling in case email is already existing
                elif tasks.Error == '2':
                    tmp_error = (error_handling_db.dbError_IntegrityError('#Task-Feedback'))
                    result[2] = tmp_error['Multiple-Records-Found']
                    return result

                # error handling in case of an compile error
                elif tasks.Error == '3':
                    tmp_error = (error_handling_db.dbError_CompileError('#Task-Feedback'))
                    result[2] = tmp_error['Compile-Error']
                    return result

                # error handling in case of a DBAPI error
                elif tasks.Error == '4':
                    tmp_error = (error_handling_db.dbError_DBAPIError('#Task-Feedback'))
                    result[2] = tmp_error['DBAPI-Error']
                    return result
                    
                # error handling in case of some other internal errors or problems
                elif tasks.Error == '5':
                    tmp_error = (error_handling_db.dbError_InternalError('#Task-Feedback'))
                    result[2] = tmp_error['Internal-Error']
                    return result
                    
                # error handling in case that more than one result were found
                elif tasks.Error == '6':
                    tmp_error = (error_handling_db.dbError_MultipleResultsFound('#Task-Feedback'))
                    result[2] = tmp_error['Multi-Records-Found']
                    return result
                    
                # error handling in case of an missing reference table error
                elif tasks.Error == '7':
                    tmp_error = (error_handling_db.dbError_NoReferencedTableError('#Task-Feedback'))
                    result[2] = tmp_error['No-Referenced-Table']
                    return result
                    
                # error handling in case that object is not executable
                elif tasks.Error == '8':
                    tmp_error = (error_handling_db.dbError_ObjectNotExecutableError('#Task-Feedback'))
                    result[2] = tmp_error['Object-Not-Executable']
                    return result
                    
                # error handling in case of other sqlalchmey errors
                elif tasks.Error == '9':
                    tmp_error = (error_handling_db.dbError_SQLAlchemyError('#Task-Feedback'))
                    result[2] = tmp_error['SQL-Alchemy-Error']
                    return result
        return result

