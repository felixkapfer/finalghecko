from os import error
from flask import render_template


def bad_request(e):
    error = {
        'error_code'      : 400,
        'error_type'      : 'Bad Request',
        'error_title'     : 'You sent a bad request',
        'error_desciption': 'Sorry, but what do you want from me - I don\'t know what \'bla bla blub\' means'
    }
    return render_template('error/base_error.html', error=error), 400

def unauthorized(e):
    error = {
        'error_code'      : 401,
        'error_type'      : 'Unauthorized',
        'error_title'     : 'Missing permissions',
        'error_desciption': 'Seems you do not have the required permission that GHECKO requires'
    }
    return render_template('error/base_error.html', error=error), 401

def forbidden(e):
    error = {
        'error_code'      : 403,
        'error_type'      : 'Forbidden',
        'error_title'     : 'Not this time, access forbidden',
        'error_desciption': 'There is no way GHECKO let you pass through'
    }
    return render_template('error/base_error.html', error=error), 403

def page_not_found(e):
    error = {
        'error_code'      : 404,
        'error_type'      : 'Page Not Found',
        'error_title'     : 'There’s no page here',
        'error_desciption': 'Looks like you ended up here by accident or this page has been swallowed by a black hole'
    }
    return render_template('error/base_error.html', error=error), 404

def method_not_allowed(e):
    error = {
        'error_code'      : 405,
        'error_type'      : 'Method not Allowed ',
        'error_title'     : 'There’s nothing here for you to see',
        'error_desciption': 'This looks like an API, so you shouldn\'t be here'
    }
    return render_template('error/base_error.html', error=error), 405








def request_timeout(e):
    error = {
        'error_code'      : 408,
        'error_type'      : 'Method not Allowed ',
        'error_title'     : 'There’s nothing here for you to see',
        'error_desciption': 'This looks like an API, so you shouldn\'t be here'
    }
    return render_template('error/base_error.html', error=error), 408

def internal_server_error(e):
    error = {
        'error_code'      : 500,
        'error_type'      : 'Method not Allowed ',
        'error_title'     : 'There’s nothing here for you to see',
        'error_desciption': 'This looks like an API, so you shouldn\'t be here'
    }
    return render_template('error/base_error.html', error=error), 500

def not_implemented(e):
    error = {
        'error_code'      : 501,
        'error_type'      : 'Method not Allowed ',
        'error_title'     : 'There’s nothing here for you to see',
        'error_desciption': 'This looks like an API, so you shouldn\'t be here'
    }
    return render_template('error/base_error.html', error=error), 501

def bad_gateway(e):
    error = {
        'error_code'      : 502,
        'error_type'      : 'Method not Allowed ',
        'error_title'     : 'There’s nothing here for you to see',
        'error_desciption': 'This looks like an API, so you shouldn\'t be here'
    }
    return render_template('error/base_error.html', error=error), 502

def service_unavailable(e):
    error = {
        'error_code'      : 503,
        'error_type'      : 'Method not Allowed ',
        'error_title'     : 'There’s nothing here for you to see',
        'error_desciption': 'This looks like an API, so you shouldn\'t be here'
    }
    return render_template('error/base_error.html', error=error), 503

def gateway_timeout(e):
    error = {
        'error_code'      : 504,
        'error_type'      : 'Method not Allowed ',
        'error_title'     : 'There’s nothing here for you to see',
        'error_desciption': 'This looks like an API, so you shouldn\'t be here'
    }
    return render_template('error/base_error.html', error=error), 504

def http_version_not_supported(e):
    error = {
        'error_code'      : 505,
        'error_type'      : 'Method not Allowed ',
        'error_title'     : 'There’s nothing here for you to see',
        'error_desciption': 'This looks like an API, so you shouldn\'t be here'
    }
    return render_template('error/base_error.html', error=error), 505
