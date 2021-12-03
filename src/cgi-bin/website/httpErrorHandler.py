from os import error
from flask import render_template


def bad_request(e):
    """
    This function is storing and returning a bad request error. It contains an error code, type, title as well as an error description.

    Args:
        e ([type]): [description]

    Returns: 
        The function returns a html template, which is filled with the specific bad request error info
    """

    error = {
        'error_code'      : 400,
        'error_type'      : 'Bad Request',
        'error_title'     : 'You sent a bad request',
        'error_desciption': 'Sorry, but what do you want from me - I don\'t know what \'bla bla blub\' means'
    }
    return render_template('main/base.error.html', error=error), 400




def unauthorized(e):
    """
    This function is storing and returning an unauthorized error. It contains an error code, type, title as well as an error description.

    Args:
        e ([type]): [description]

    Returns: 
        The function returns a html template, which is filled with the specific unauthorized error info
    """

    error = {
        'error_code'      : 401,
        'error_type'      : 'Unauthorized',
        'error_title'     : 'Missing permissions',
        'error_desciption': 'Seems you do not have the required permission that GHECKO requires'
    }
    return render_template('main/base.error.html', error=error), 401




def forbidden(e):
    """
    This function is storing and returning a forbidden error. It contains an error code, type, title as well as an error description.

    Args:
        e ([type]): [description]

    Returns:
        The function returns a html template, which is filled with the specific forbidden error info
    """

    error = {
        'error_code'      : 403,
        'error_type'      : 'Forbidden',
        'error_title'     : 'Not this time, access forbidden',
        'error_desciption': 'There is no way GHECKO let you pass through'
    }
    return render_template('main/base.error.html', error=error), 403




def page_not_found(e):
    """
    This function is storing and returning a page not found error. It contains an error code, type, title as well as an error description.

    Args:
        e ([type]): [description]

    Returns:
        The function returns a html template, which is filled with the specific page not found error info
    """

    error = {
        'error_code'      : 404,
        'error_type'      : 'Page Not Found',
        'error_title'     : 'There’s no page here',
        'error_desciption': 'Looks like you ended up here by accident or this page has been swallowed by a black hole'
    }
    return render_template('main/base.error.html', error=error), 404




def method_not_allowed(e):
    """
    This function is storing and returning a method not allowed error. It contains an error code, type, title as well as an error description.

    Args:
        e ([type]): [description]

    Returns:
        The function returns a html template, which is filled with the specific method not allowed error info
    """

    error = {
        'error_code'      : 405,
        'error_type'      : 'Method not Allowed ',
        'error_title'     : 'There’s nothing here for you to see',
        'error_desciption': 'This looks like an API, so you shouldn\'t be here'
    }
    return render_template('main/base.error.html', error=error), 405





def request_timeout(e):
    """
    This function is storing and returning a request timeout error. It contains an error code, type, title as well as an error description.

    Args:
        e ([type]): [description]

    Returns:
        The function returns a html template, which is filled with the specific request timeout error info
    """

    error = {
        'error_code'      : 408,
        'error_type'      : 'Request Timeout ',
        'error_title'     : 'We ended in a request timeout',
        'error_desciption': 'Sorry! Our request did take too long. Please try again.'
    }
    return render_template('main/base.error.html', error=error), 408




def internal_server_error(e):
    """
    This function is storing and returning an internal server error. It contains an error code, type, title as well as an error description.

    Args:
        e ([type]): [description]

    Returns:
        The function returns a html template, which is filled with the specific internal server error info
    """

    error = {
        'error_code'      : 500,
        'error_type'      : 'Internal Server Error ',
        'error_title'     : 'Houston we got a problem',
        'error_desciption': 'Sorry, we do have an internal Server Error. We are trying to fix this.'
    }
    return render_template('main/base.error.html', error=error), 500




def not_implemented(e):
    """
    This function is storing and returning a not implemented error. It contains an error code, type, title as well as an error description.

    Args:
        e ([type]): [description]

    Returns:
        The function returns a html template, which is filled with the specific not implemented error info
    """

    error = {
        'error_code'      : 501,
        'error_type'      : 'Not implemented ',
        'error_title'     : 'There’s nothing here for you to see',
        'error_desciption': 'We do not have this function. We\'re sorry!'
    }
    return render_template('main/base.error.html', error=error), 501




def bad_gateway(e):
    """
    This function is storing and returning a bad gateway error. It contains an error code, type, title as well as an error description.

    Args:
        e ([type]): [description]

    Returns:
        The function returns a html template, which is filled with the specific bad gateway error info
    """

    error = {
        'error_code'      : 502,
        'error_type'      : 'Bad Gateway ',
        'error_title'     : 'Bad Gateway',
        'error_desciption': 'Ups! Something went wrong. Please try again'
    }
    return render_template('main/base.error.html', error=error), 502




def service_unavailable(e):
    """
    This function is storing and returning a service unavailable error. It contains an error code, type, title as well as an error description.

    Args:
        e ([type]): [description]

    Returns:
        The function returns a html template, which is filled with the specific service unavailable error info
    """

    error = {
        'error_code'      : 503,
        'error_type'      : 'Service Unavailable ',
        'error_title'     : 'Not possible',
        'error_desciption': 'This service is not available.'
    }
    return render_template('main/base.error.html', error=error), 503




def gateway_timeout(e):
    """
    This function is storing and returning a bgateway timeout error. It contains an error code, type, title as well as an error description.

    Args:
        e ([type]): [description]

    Returns:
       The function returns a html template, which is filled with the specific gateway timeout error info
    """

    error = {
        'error_code'      : 504,
        'error_type'      : 'Gateway timeout ',
        'error_title'     : 'Too long',
        'error_desciption': 'We have a gateway timeout. We are sorry. Please try again'
    }
    return render_template('main/base.error.html', error=error), 504




def http_version_not_supported(e):
    """
    This function is storing and returning a http version not supported error. It contains an error code, type, title as well as an error description.

    Args:
        e ([type]): [description]

    Returns:
        The function returns a html template, which is filled with the specific http version not supported error info
    """

    error = {
        'error_code'      : 505,
        'error_type'      : 'HTTP Version not supported',
        'error_title'     : 'Wrong Version',
        'error_desciption': 'This version of HTTP is not supported. Please check and then try again.'
    }
    return render_template('main/base.error.html', error=error), 505
