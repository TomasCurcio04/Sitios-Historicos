from flask import Flask

def create_app(env, static_folder):
    app = Flask(__name__)

    @app.route('/')
    def home():
        return 'Hello, World!'
    
    return app