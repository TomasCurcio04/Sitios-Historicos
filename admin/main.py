from src.web import create_app

if __name__ == "__main__":
    app = create_app(env="development", static_folder="")
    app.run(debug=True)
