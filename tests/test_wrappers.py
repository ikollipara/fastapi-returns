# tests/test_async_wrapper.py
# Ian Kollipara
# 2022.01.19
#
# Testing Future and IO

# Imports
from typing import Any
import pytest
from returns import future, io, maybe
from fastapi_returns import _wrappers
from fastapi import HTTPException


@pytest.mark.anyio
async def test_future_wrapper_for_zero_params():
    def zero_future_func() -> future.Future[str]:
        return future.Future.from_value("Test")
    
    
    result = (await zero_future_func().awaitable())._inner_value

    new_func_result = await _wrappers.future_wrapper(zero_future_func)()

    assert result == new_func_result

@pytest.mark.parametrize("test_args", [1, [1,2], [1,2,3], [1,2,3,4]])
@pytest.mark.anyio
async def test_future_wrapper_for_many_params(test_args):
    def many_future_func(*args) -> future.Future[Any]:
        return future.Future.from_value(args)

    result = (await many_future_func(test_args).awaitable())._inner_value

    new_func_result = await _wrappers.future_wrapper(many_future_func)(test_args)
    
    assert result == new_func_result

def test_io_wrapper_for_zero_params():
    def zero_io_func() -> io.IO[str]:
        return io.IO("test")
    
    res = zero_io_func()._inner_value

    new_func_result = _wrappers.io_wrapper(zero_io_func)()

    assert res == new_func_result

@pytest.mark.parametrize("test_args", [1, [1,2], [1,2,3], [1,2,3,4]])
def test_io_wrapper_for_many_params(test_args):
    def many_io_func(*args) -> io.IO[Any]:
        return io.IO(args)
    
    res = many_io_func(test_args)._inner_value

    new_func_result = _wrappers.io_wrapper(many_io_func)(test_args)

    assert res == new_func_result

def test_maybe_wrapper_for_zero_params_some():
    def zero_maybe_func() -> maybe.Maybe[str]:
        return maybe.Some("test")
    
    res = zero_maybe_func()._inner_value

    new_func_result = _wrappers.maybe_wrapper(zero_maybe_func)()


    assert res == new_func_result

@pytest.mark.parametrize("test_args", [1, [1,2], [1,2,3], [1,2,3,4]])
def test_maybe_wrapper_for_many_params_some(test_args):
    def many_maybe_func(*args) -> maybe.Maybe[Any]:
        return maybe.Some(args)
    
    res = many_maybe_func(test_args)._inner_value

    new_func_result = _wrappers.maybe_wrapper(many_maybe_func)(test_args)

    assert res == new_func_result

def test_maybe_wrapper_for_zero_params_nothing():
    def zero_maybe_func() -> maybe.Maybe[Any]:
        return maybe.Nothing
    
    with pytest.raises(HTTPException):
        _wrappers.maybe_wrapper(zero_maybe_func)()

@pytest.mark.parametrize("test_args", [1, [1,2], [1,2,3], [1,2,3,4]])
def test_maybe_wrapper_for_many_params_nothing(test_args):
    def many_maybe_func(*args) -> maybe.Maybe[Any]:
        return maybe.Nothing
    
    with pytest.raises(HTTPException):
        _wrappers.maybe_wrapper(many_maybe_func)(test_args)