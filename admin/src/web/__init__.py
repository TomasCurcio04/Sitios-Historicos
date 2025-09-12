from flask import Flask, render_template
import os
from src.web.handlers import error

def create_app(env="development", static_folder=None):
    if not static_folder:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        static_folder = os.path.abspath(os.path.join(base_dir, "..", "..", "static"))

    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
        static_folder=static_folder
    )

    @app.route('/')
    def home():
        return render_template("home.html")
    
    app.register_error_handler(404, error.not_found)
    app.register_error_handler(403, error.not_authorized)
    app.register_error_handler(500, error.internal_server_error)
    
    return app
