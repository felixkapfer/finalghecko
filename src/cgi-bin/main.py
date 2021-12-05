import dependencies                 #import dependencies for projektmanagement-ghecko.de
from website import createApp

app = createApp()

if __name__ == '__main__':
    app.run(debug=True)