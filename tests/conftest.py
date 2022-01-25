# tests/conftest.py
# Ian Kollipara
# 2022.01.19
#
# Pytest Fixture

# Imports
from pytest import fixture
from fastapi import FastAPI, testclient
from fastapi_returns.returns_router import ReturnsRouter
from returns import future

@fixture
def client():
    app = FastAPI()

    router = ReturnsRouter()

    @router.get("/")
    def func() -> str:
        return "test"
    
    @router.get("/future")
    def func2() -> future.Future[str]:
        return future.Future.from_value("test")

    app.include_router(router)

    return testclient.TestClient(app)

