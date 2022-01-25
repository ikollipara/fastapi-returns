import pytest
from fastapi_returns_router.returns_router import ReturnsRouter 
from fastapi.testclient import TestClient
from fastapi import FastAPI

def test_router_usage(client: TestClient):

    res = client.get("/")

    assert res.status_code == 200
    assert "test" in res.text

def test_wrapper_in_router(client: TestClient):
    
    res = client.get("/future")

    assert res.status_code == 200
    assert "test" in res.text

def test_untyped_route_fail():
    app = FastAPI()

    router = ReturnsRouter()
    
    with pytest.raises(ValueError):
        router.get("/")(lambda: "test")