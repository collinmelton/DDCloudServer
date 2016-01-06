from WebApp import app

# if __name__ == "__main__":
#     from werkzeug.debug import DebuggedApplication
#     app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
#     app.run(debug=True)
    
if __name__ == '__main__':
    import logging
    logging.basicConfig()
    app.run(debug=False) # debug must be off on production for security reasons