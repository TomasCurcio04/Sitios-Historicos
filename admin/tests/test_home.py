from src.web import create_app


app = create_app(env="testing")
app.testing = True
client = app.test_client()

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "<h2>¡Hola mundo!</h2>" in response.data.decode("utf-8")
