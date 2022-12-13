from flask import Flask, redirect

def create_app():
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return redirect("/api/users")

    # main api route
    from . import index
    app.register_blueprint(index.api)

    return app