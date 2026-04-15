import pytest
import requests

BASE_URL = "http://localhost:5000"  # change if your API uses a different port


# ✅ TEST 1: VALID RESPONSE (200)
def test_valid_response():
    response = requests.get(f"{BASE_URL}/api/users")  # change endpoint if needed

    print("Status Code:", response.status_code)
    assert response.status_code == 200


# ❌ TEST 2: INVALID RESPONSE (401)
def test_invalid_response():
    headers = {
        "Authorization": "Bearer invalid_token"
    }

    response = requests.get(f"{BASE_URL}/api/users", headers=headers)

    print("Status Code:", response.status_code)
    assert response.status_code == 401
