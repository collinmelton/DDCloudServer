from WebApp import app

if __name__ == "__main__":
    from werkzeug.debug import DebuggedApplication
    app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
    app.run(debug=True)