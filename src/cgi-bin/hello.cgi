#!/usr/bin/python3
# startpoint for projektmanagement-ghecko.de

try:   
    from wsgiref.handlers import CGIHandler
    from main import app

    CGIHandler().run(app)
except Exception as err:
    print("Content-Type: text/html/n/")
    print(err)