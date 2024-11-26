# tests/test_predict.py

def test_predict(test_client):
    response = test_client.post(
        "/api/v1/predict/",
        json={
            "fixed_acidity": 7.4,
            "volatile_acidity": 0.70,
            "citric_acid": 0.00,
            "residual_sugar": 1.9,
            "chlorides": 0.076,
            "free_sulfur_dioxide": 11.0,
            "total_sulfur_dioxide": 34.0,
            "density": 0.9978,
            "pH": 3.51,
            "sulphates": 0.56,
            "alcohol": 9.4
        }
    )
    assert response.status_code == 200
    assert "quality" in response.json()
