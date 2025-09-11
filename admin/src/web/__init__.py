from flask import Flask, render_template
import os

def create_app(env="development", staticfolder=""):
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
        static_folder=staticfolder
    )

    @app.route('/')
    def home():
        return render_template("home.html")
    
    return app
