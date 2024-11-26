# tests/test_main.py

def test_read_main(test_client):
    response = test_client.get("/")
    assert response.status_code == 404  # Ajusta según tus rutas
