from fastapi.testclient import TestClient
from csgoscan.main import app
import pytest

client = TestClient(app)

profiles = [
    ("/profiles/76561198069504185", 200),
    ("/profiles/76561199238664674", 200),
]


@pytest.mark.parametrize("profile,expected", profiles)
def test_profile(profile, expected):
    response = client.get(profile)
    assert response.status_code == expected
