from flask import Flask, abort ,render_template
import os
from src.web.handlers import error
from src.web.controllers.issues import bp as issues_bp
from src.web.config import config


def create_app(env="development", static_folder=None):
    if not static_folder:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        static_folder = os.path.abspath(os.path.join(base_dir, "..", "..", "static"))

    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
        static_folder=static_folder
    )
    app.config.from_object(config[env])
    print(app.config)

    @app.route('/')
    def home():
        return render_template("home.html")
    
     #Registrar blueprints
    app.register_blueprint(issues_bp)
    
    #Manejo de errores
    app.register_error_handler(404, error.not_found)
    app.register_error_handler(401, error.not_authorized)
    app.register_error_handler(500, error.internal_server_error)

   
    
    return app
