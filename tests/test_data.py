import requests
import json

def test_data_endpoint():
    response = requests.get("http://127.0.0.1:8000/data/all")
    assert response.status_code == 200
    data = response.json()
    assert "businesses" in data
    assert isinstance(data["businesses"], list)
    assert len(data["businesses"]) > 0
    # Validate JSON structure
    for business in data["businesses"]:
        assert "name" in business
        assert "streetAddress" in business
        assert "cityStateZip" in business
        assert "phoneNumber" in business
        assert "website" in business
        assert "imageURL" in business
        assert "membershipLevel" in business
        assert "adcopy" in business

def test_data_json_valid():
    response = requests.get("http://127.0.0.1:8000/data/all")
    assert response.status_code == 200
    try:
        json.loads(response.text)
    except json.JSONDecodeError:
        assert False, "Response is not valid JSON"

def test_end_to_end():
    # First authenticate
    auth_response = requests.get("http://127.0.0.1:8000/users/?username=admin&password=qwerty")
    assert auth_response.status_code == 200
    # Then get data
    data_response = requests.get("http://127.0.0.1:8000/data/all")
    assert data_response.status_code == 200
    data = data_response.json()
    assert len(data["businesses"]) == 9  # Based on the hardcoded data