"""
    author: Felix Kapfer
    date: 12.11.2021
    license: private
"""
from flask import json

#This function is used to store the error messages and customize it for the output section. 
            #Gets executed if no results were found in db

class DbError():
    """This class defines various methods used for error handling. 
        
       This class contains the following methods
       which store the messages to be printed out for the user in case the specified error occurs:
       
       * dbError_noResultFound
       * dbError_IntegrityError
       * dbError_CompileError
       * dbError_DBAPIError
       * dbError_InternalError
       * dbError_MultipleResultsFound
       * dbError_NoReferencedTableError
       * dbError_ObjectNotExecutableError 
       * dbError_SQLAlchemyError

    """
    def dbError_noResultFound(self, output):
        """This function is used to store the error message for the No Results Found Error.
        Args:
            output (String):  HTML Id of the div Box

        Returns:
            JSON objects: information about the error and the error message in JSON format
            

        Test:
            * Test 1: test if the given parameter is added to error and displayed correctly
            * Test 2: test behaviour if the parameter is not string but another datatype 
            * Test 3 test what happens when the quote marks are missing
            * Test 4:  test behaviour when multiple parameters are given instead of one
            * Test 5: test test if the error object is correctly saved and returned
            * Test 6: test if both parts of the error object function correctly.ö

        """
        error = {
            'No-Result-Found' : {
                'Error-Code' : '01-1',
                'Error-Type' : 'No-Result-Found:',
                'Render-Output' : output,
                'Description' : 'Mhhh... It seems you do not have submitted any data yet',
                'Excuse': 'We are sorry, but it seems we do not have any records about the requested source.'
            },
            'No-User-Found' : {
                'Error-Code' : '01-2',
                'Error-Type' : 'No-User-Found:',
                'Render-Output' : output,
                'Description' : 'Mhhh... It seems you do not have any account yet - Please create one first, before you try to log-in',
                'Excuse': 'We are sorry, but it seems we do not have any records about the requested source.'
            }
        }
        return error

    def dbError_IntegrityError(self, output):
        """ This function is used to store the error messages for the Integrity Error.
        Args:
            output (String):  HTML Id of the div Box

        Returns:
            JSON objects: information about the error and the error message in JSON format
            
        Tests: 
            * Test 1: test behaviour if the parameter is not string but another datatype and test what happens when the quote marks are missing
            * Test 2: test behaviour when multiple parameters are given instead of one
            * Test 3: test if the given parameter is added to error correctly, and test test if the error object is correctly returned
            
        """
        error = {
            'Multiple-Records-Found' : {
                'Error-Code' : '02-1',
                'Error-Type' : 'Already-Existing-Record-Found:',
                'Render-Output' : output,
                'Description' : 'Mhhh... It seems a similar record is already existing but has to be unique! Therefore your record-submission failed!',
                'Excuse' : 'We are sorry, but it seems a similar record is already existing.'
            },
            'Multiple-Users-Found' : {
                'Error-Code' : '02-2',
                'Error-Type' : 'Already-Existing-User-Found:',
                'Render-Output' : output,
                'Description' : 'Mhhh... It seems that this E-Mail Address is already in use and therefore not available for registration!',
                'Excuse': 'We are sorry, but it seems this email is already taken.'
            }
        }
        return error

    def dbError_CompileError(self, output):
        """This function is used to store the error message for the Compile Error.
        Args:
            output (String):  HTML Id of the div Box

        Returns:
            JSON object: information about the error and the error message in JSON format
            
        Tests: 
            * Test 1: test behaviour if the parameter is not string but another datatype and test what happens when the quote marks are missing
            * Test 2: test behaviour when multiple parameters are given instead of one
            * Test 3: test if the given parameter is added to error correctly, and test whether the error object is correctly returned
            * Test 4: test if the json format works correctly on the site
            """
        error = {
            'Compile-Error' : {
                'Error-Code' : '03-1',
                'Error-Type' : 'Compile Error:',
                'Render-Output' : output,
                'Description' : 'Mhhh... It seems an error occured during SQL compilation.   Therefore your request could not be executed.',
                'Excuse': 'We are sorry, but it seems  an error occured during SQL compilation.'
            }
        }
        return error

    def dbError_DBAPIError(self, output):
        """This function is used to store the error message for the DBAPI Error.
        Args:
            output (String):  HTML Id of the div Box

        Returns:
            JSON object: information about the error and the error message in JSON format
            
        Tests: 
            * Test 1: test if the error object is returned and displayed correctly 
            * Test 2: test behaviour when multiple parameters are given instead of one
            * Test 3: test if the json format works correctly on the site
            """
        error = {
            'DBAPI-Error' : {
                'Error-Code' : '04-1',
                'Error-Type' : 'DBAPI-Error:',
                'Render-Output' : output,
                'Description' : 'Mhhh... It seems  there is an error from the DB-API. The execution of the database operation failed!',
                'Excuse' : 'We are sorry, but it seems there is an error from the DB-API.'
            }
        }
        return error

    def dbError_InternalError(self, output):
        """This function is used to store the error message for the DBAPI Internal Error.
        Args:
            output (String):  HTML Id of the div Box

        Returns:
            JSON object: information about the error and the error message in JSON format
        
        Tests: 
            * Test 1: test behaviour when multiple or no parameters are given instead of one
            * Test 2: test if the error object is returned and displayed as expected   
        """
        error = {
            'Internal Error' : {
                'Error-Code' : '05-1',
                'Error-Type' : 'Internal Error:',
                'Render-Output' : output,
                'Description' : 'Mhhh... It seems an internal error occurred in the DB!',
                'Excuse': 'We are sorry, but it seems there is an internal error in the DB.'
            }
        }
        return error

    def dbError_MultipleResultsFound(self, output):
        """This function is used to store the error messages for the Multiple Results Found Error. 
        Args:
            output (String):  HTML Id of the div Box

        Returns:
            JSON objects: information about the error and the error messages in JSON format
            
        Test:
            * Test 1: test behaviour if there is a missing or too many parameter given
            * Test 2: test if the given parameter is added to error object correctly, and test if the error object is correctly returned         
        """
        error = {
            'Multi-Records-Found' : {
                'Error-Code' : '06-1',
                'Error-Type' : 'Multi-Records-Found:',
                'Render-Output' : output,
                'Description' : 'Mhhh... It seems a single database result was asked for but more than one were found.',
                'Excuse' : 'We are sorry, but it seems there are multiple records.'
            },
            'Multi-User-Found' : {
                'Error-Code' : '06-2',
                'Error-Type' : 'Multi-User-Found:',
                'Render-Output' : output,
                'Description' : 'Mhhh... It seems you asked for a single user but more than one were found.',
                'Excuse' : 'We are sorry, but it seems there are several users instead of one.'
            }
        }
        return error

    def dbError_NoReferencedTableError(self, output):
        """This function is used to store the error message for the No-Referenced-Table-Error. 
        Args:
            output (String):  HTML Id of the div Box

        Returns:
            JSON object: information about the error and the error message in JSON format
        
        Test:
            * Test 1: test the behaviour if different datatypes are given
            * Test 2: test if all parts of the error message are returned as expected
            """
        error = {
            'No-Referenced-Table' : {
                'Error-Code' : '07-1',
                'Error-Type' : 'No-Referenced-Table:',
                'Render-Output' : output,
                'Description' : 'Mhhh... It seems a foreign key triggered this error since the referred table could not be found.',
                'Excuse' : 'We are sorry, but a table referenced through a foreign key could not be located.'
            }
            
        }
        return error

    def dbError_ObjectNotExecutableError(self, output):
        """This function is used to store the error message for the Object-Not-Executable-Error. 
        Args:
            output (String):  HTML Id of the div Box

        Returns:
            JSON object: information about the error and the error message in JSON format
            
        Test:
            * Test 1: test the behaviour if different datatypes are given
            * Test 2: test if all parts of the error message are returned as expected 
        """
        error = {
            'Object-Not-Executable' : {
                'Error-Code' : '08-1',
                'Error-Type' : 'Object-Not-Executable',
                'Render-Output' : output,
                'Description' : 'Mhhh... It seems an object was passed to .execute() and it can’t be executed as SQL.',
                'Excuse' : 'We are sorry but this object can not be executed.'
            }
        }
        return error

    def dbError_SQLAlchemyError(self, output):
        """This function is used to store the error message for the SQL-Alchemy-Error(generic error class). 
        Args:
            output (String):  HTML Id of the div Box

        Returns:
            JSON object: information about the error and the error message in JSON format
         
        Tests:    
            * Test 1: test the behaviour if different datatypes are given
            * Test 2: test if all parts of the error message are returned as expected
        """
        error = {
            'SQL-Alchemy-Error' : {
                'Error-Code' : '10-1',
                'Error-Type' : 'SQL-Alchemy-Error:',
                'Render-Output' : output,
                'Description' : 'Mhhh... It seems something went wrong in SQL Alchemy.A not further specified error occured.     ',
                'Excuse' : 'We are sorry but an unspecified error occured.'
            }
        }
        return error

class FormError():
    """This class defines various methods used for error handling of errors regarding an unallowed form of the input data given by a user. 
        
       This class contains the following methods
       which store the messages to be printed out for the user in case the specified error occurs:
       
       * formError_invalidTypeError
       * formError_invalidLength
       * formError_invalidEmail
       * formError_invalidPassword
    """
    def formError_invalidTypeError(self, output, target='', data_type_given='', data_type_expected=''):
        """This function is used to store the error messages regarding invalid input from the user, 
            specifically an invalid form or datatypes.

        Args:
            output (str):  HTML Id of the div Box
            target (str, optional): The input the user is tying to give -e.g a password or an username or an email. Defaults to ''.
            data_type_given (str, optional): The type of data given by the user. Defaults to ''.
            data_type_expected (str, optional): The type of data needed from the user. Defaults to ''.

        Returns:
            error(JSON objects): information about the error and the error message in JSON format
            
        Tests:
            * Test 1: test if the input parameters are correctly identified, test what happens if they are given in the wrong order
            * Test 2: test if all parts of the error message are returned as expected
        
        """
        error = {
            'Invalid-Format' : {
                'Error-Code'   : '11-1',
                'Error-Type'   : 'Invalid-Type-Failure:',
                'Render-Output': output,
                'Description'  : "Invalid type of Input: Type of Input given: " + data_type_given + ' <br>Type of Input is expected to be: ' + data_type_expected
            },
            'Invalid-Arguments': {
                'Error-Code'   : '11-2',
                'Error-Type'   : 'Invalid-Type-Failure:',
                'Render-Output': output,
                'Description'  : target + ' can only contain ' + data_type_expected + '!'
            },
            'Missing-Arguments': {
                'Error-Code'   : '11-3',
                'Error-Type'   : 'Missing-Required-Arguments-Failure:',
                'Render-Output': output,
                'Description'  : target + ' has to contain at least ' + data_type_expected + '!'
            }
        }
        return error

    def formError_invalidLength(self, output, number_of_chars, target, description):
        """This function is used to store the error messages regarding invalid input from the user, 
            which is invalid because of its length or because it is void.


        Args:
            output (str):  HTML Id of the div Box
            number_of_chars (int): the required number of characters of the input the user is tying to give
            target (str): The input the user is tying to give -e.g a password or an username or an email. 
            description (str):  a description regarding the error

        Returns:
            error(JSON object): information about the error and the error message in JSON format
            
        Tests:
            * Test 1: test if the input parameters are correctly identified, test what happens if they are given in the wrong order, or when not all of them are given
            * Test 2: test if all parts of the error message are returned as expected    
        """
        error = {
            'Invalid-Empty-String' : {
                'Error-Code'   : '12-1',
                'Error-Type'   : 'Missing-Data-Failure:',
                'Render-Output': output,
                'Description'  : description
            },
            'Invalid-Minimum-Of-Length' : {
                'Error-Code'   : '12-2',
                'Error-Type'   : 'Out-Of-Minimum-Length-Failure:',
                'Render-Output': output,
                'Description'  : target + ' must contain at least ' + number_of_chars + ' charactes!'
            },
            'Invalid-Maximum-Of-Length': {
                'Error-Code'   : '12-3',
                'Error-Type'   : 'Out-Of-Maximum-Length-Failure:',
                'Render-Output': output,
                'Description'  : target + ' cannot contain more than ' + number_of_chars + ' charactes!'
            }
        }
        return error

    def formError_invalidEmail(self, output):
        """This function is used to store the error messages regarding invalid input from the user for the email field , 
            which is invalid because of its format or because the email is already taken.

        Args:
            output (str):  HTML Id of the div Box

        Returns:
            error (JSON object): information about the error and the error message in JSON format
            
        Tests:
            * Test 1: test whether both parts of the error object are accessible
            * Test 2: test if the error object is returned and displayed as expected   
        """
        error = {
            'Invalid-Format' : {
                'Error-Code' : '13-1',
                'Error-Type' : 'Invalid-Email-Failure:',
                'Render-Output' : output,
                'Description' : 'Incorrect E-Mail Format! - Please enter the correct format!'
            },
            'Already-Taken': {
                'Error-Code' : '13-2',
                'Error-Type' : 'Unique-Failure:',
                'Render-Output' : output,
                'Description' : 'E-Mail is already taken!'
            }
        }
        return error


    def formError_invalidPassword(self, output):
        """This function is used to store the error messages regarding invalid input from the user for the password field , 
            which is invalid either because the same characters are used for another field (e.g. email or name) 
            or the passwods don't match or because the user's combination of email and password is not valid.
            
        Args:
            output  (str):  HTML Id of the div Box

        Returns:
            error (JSON object): information about the error and the error message in JSON format
            
        Tests:
            * Test 1:  test behaviour when multiple parameters are given instead of one
            * Test 2: test if the given parameter is added to error correctly, and test whether the error object is returned correctly 
                  
        """
        error = {
            'Invalid-Format': {
                'Error-Code' : '14-1',
                'Error-Type' : 'Unique-Failure:',
                'Render-Output' : output,
                'Description' : 'Password cannot contain Firstname, Lastname or your E-Mail address!'
            },
            'Confirmation-Error' : {
                'Error-Code' : '14-2',
                'Error-Type' : 'Confirmation-Failure:',
                'Render-Output' : output,
                'Description' : 'Passwords do not match, please try again!'
            },
            'Login-Error' : {
                'Error-Code' : '14-3',
                'Error-Type' : 'Invalid-Credentials:',
                'Render-Output' : output,
                'Description' : 'Invalid E-Mail Address or Password!'
            }
        }
        return error
        
    