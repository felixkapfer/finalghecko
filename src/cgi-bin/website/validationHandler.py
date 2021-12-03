import re


class Validation():
    def validation_isEmpty(self, data):
        """This method can be called to validate if a variable contains any content e.g. letters, numbers, dates, etc.  

        Args:
            data (ImmutableMultiDict): Contains data that should be verified that a variable contains some data

        Returns:
            boolean: Return True if the variable is empty or only contains spaces and returns False if the variable contains some value 
        """
        if data and data.strip():
            return False
        else:
            return True




    def validation_minLength(self, data, min_length):
        """This method can be called to validate that a variable has a minimum length

        Args:
            min_length (int): Contains the number of the minimun length
            data (ImmutableMultiDict): Contains data that should be verified that a variable contains some data

        Returns:
            boolean: Return True if the variables length is greater than or equal to the min_length and returns False if the variables length is less than the min_length
        """
        length = len(data)
        if length >= min_length:
            return True
        else:
            return False




    def validation_maxLength(self, data, max_length):
        """This method can be called to validate that a variable has a maximum length

        Args:
            data (ImmutableMultiDict): Contains data that should be verified that a variable contains some data
            max_length (int): Contains the number of the maximum length

        Returns:
            boolean: Return True if the variables length is less than or equal to the max_length and returns False if the variables length is greater than the max_length
        """
        legth = len(data)
        if legth <= max_length:
            return True
        else:
            return False




    def validation_isAlphaNum(self, data):
        """This method can be called to validate that a variable only contains alphanumerics. A character which is either a letter or a number is known as alphanumeric.

        Args:
            data (ImmutableMultiDict): Contains data that should be verified that a variable contains some data

        Returns:
            boolean: Return True if the variable only contains alphanumerics and returns False if the variable does not only contain alphanumerics
        """
        if data.isalnum():
            return True
        else:
            return False




    def validation_isAlpha(self, data):
        """This method can be called to validate that a variable only contains aplhabets.

        Args:
            data (ImmutableMultiDict): Contains data that should be verified that a variable contains some data

        Returns:
            boolean: Return True if the variable only contains alphabets and returns False if the variable does not only contain alphabets
        """
        if data.isalpha():
            return True
        else:
            return False
            



    def validation_isAlphaWithSpaces(self, data):
        """This method can be called to validate that a variable only contains aplhabets.

        Args:
            data (ImmutableMultiDict): Contains data that should be verified that a variable contains some data

        Returns:
            boolean: Return True if the variable only contains alphabets or spaces between alpahbets and returns False if the variable does not only contain alphabets
        """
        data = data.strip()
        if all(x.isalpha() or x.isspace() for x in data):
            return True
        else:
            return False
            



    def validation_isEmail(self, data):
        """This method can be called to validate if a variable has a certain pattern

        Args:
            data (ImmutableMultiDict): Contains data that should be verified that a variable contains some data

        Returns:
            boolean: Return True if the variable has that certain pattern and Return False if it does not have that pattern
        """
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
        if(re.search(regex, data)):   
            return True
        else:
            return False




    def validation_containsUpperChar(self, data):
        """This method can be called to validate if a variable contains any upper case characters

        Args:
            data (ImmutableMultiDict): Contains data that should be verified that a variable contains some data

        Returns:
            boolean: Return True if the variable contains any upper case characters and Return False if it does not contain any upper case characters
        """
        if any(char.isupper() for char in data):
            return True 
        else:
            return False




    def validation_containsLowerChar(self, data):
        """This method can be called to validate if a variable contains any lower case characters

        Args:
            data (ImmutableMultiDict): Contains data that should be verified that a variable contains some data

        Returns:
            boolean: Return True if the variable contains any lower case characters and Return False if it does not contain any lower case characters
        """
        if any(char.islower() for char in data):
            return True 
        else:
            return False




    def validation_containsDigit(self, data):
        """This mehtod can be called to validate if a variable contains one or more digits.

        Args:
            data (ImmutableMultiDict): Contains data that should be verified that a variable contains some data

        Returns:
            boolean: Return True if the variable contains one or more digits and Return False if the variable does not contain a digit.
        """
        if any(char.isdigit() for char in data):
            return True 
        else:
            return False




    def validation_containsSpecialChar(self, data):
        """This mehtod can be called to validate if a variable contains any special characters.

        Args:
            data (ImmutableMultiDict): Contains data that should be verified that a variable contains some data

        Returns:
            boolean: Return True if the variable contains any special characters and Return False if the variable does not contain any special characters.
        """
        specialChar = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
        if any(char in specialChar for char in data):
            return True
        else:
            return False




    def validation_followPasswordRequlations(self, pwd, firstname, lastname, email):
        """This mehtod can be called to validate if the password contains 'admin' or 'adm' or 'administrator' or 'strator' or 'default' or 'master' or firstname or eamil or lastname 

        Args:
            pwd (ImmutableMultiDict): Contains the password the user enters
            firstname (ImmutableMultiDict): Contains the firstname the user enters
            lastname (ImmutableMultiDict): Contains the lastname the user enters
            email (ImmutableMultiDict): Contains the email the user enters

        Returns:
            boolean: Return True if the password contains 'admin' or 'adm' or 'administrator' or 'strator' or 'default' or 'master' or firstname or email or lastname and Return False if the variable does not contain any of these
        """
        pwd       = pwd.lower()
        firstname = firstname.lower()
        email     = email.lower()
        lastname  = lastname.lower()
        # if 'admin' in pwd or 'adm' in pwd or 'administrator' in pwd or 'strator' in pwd or 'default'  or 'master' in pwd or firstname in pwd or email in pwd or lastname in pwd:
        if 'admin' in pwd:
            return True
        else:
            return False