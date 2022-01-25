# tests/test_result_wrappers.py
# Ian Kollipara
# 2022.01.19
#
# Testing Result, IOResult, and FutureResult

# Imports
from typing import Any, List
from fastapi_returns import _wrappers
from returns import result, future, io
import pytest


@pytest.mark.anyio
async def test_future_result_wrapper_for_zero_params_success():
    def zero_future_result_func_success() -> future.FutureResult[str, Exception]:
        return future.FutureSuccess("test")
    
    result = (await zero_future_result_func_success().awaitable())._inner_value._inner_value

    new_func_result = await _wrappers.future_result_wrapper(zero_future_result_func_success)()

    assert result == new_func_result

@pytest.mark.anyio
async def test_future_result_wrapper_for_zero_params_failure():
    def zero_future_result_func_failure() -> future.FutureResult[str, Exception]:
        return future.FutureFailure(ValueError("test"))

    with pytest.raises(ValueError):
        await _wrappers.future_result_wrapper(zero_future_result_func_failure)()

    with pytest.raises(ValueError):
        raise (await zero_future_result_func_failure().awaitable())._inner_value._inner_value
    

@pytest.mark.parametrize("test_args", [1, [1,2], [1,2,3], [1,2,3,4]])
@pytest.mark.anyio
async def test_future_result_wrapper_for_many_params_success(test_args):
    def many_future_result_func_success(*args) -> future.FutureResult[Any, Exception]:
        return future.FutureSuccess(args)
    
    result = (await many_future_result_func_success(test_args).awaitable())._inner_value._inner_value

    new_func_result = await _wrappers.future_result_wrapper(many_future_result_func_success)(test_args)

    assert result == new_func_result

@pytest.mark.parametrize("test_args", [1, [1,2], [1,2,3], [1,2,3,4]])
@pytest.mark.anyio
async def test_future_result_wrapper_for_many_params_failure(test_args):
    def zero_future_result_func_failure(*args) -> future.FutureResultE[Any]:
        return future.FutureFailure(ValueError("test"))

    with pytest.raises(ValueError):
        await _wrappers.future_result_wrapper(zero_future_result_func_failure)(test_args)

    with pytest.raises(ValueError):
        raise (await zero_future_result_func_failure(test_args).awaitable())._inner_value._inner_value
    

    
def test_result_wrapper_for_zero_params_success():
    def zero_result_func_success() -> result.Result[str, Exception]:
        return result.Result.from_value("test")
    
    res = zero_result_func_success()._inner_value

    new_func_result = _wrappers.result_wrapper(zero_result_func_success)()

    assert res == new_func_result

@pytest.mark.parametrize("test_args", [1, [1,2], [1,2,3], [1,2,3,4]])
def test_result_wrapper_for_many_params_success(test_args):
    def many_result_func_success(*args) -> result.ResultE[Any]:
        return result.Result.from_value(args)
    
    res = many_result_func_success(test_args)._inner_value

    new_func_result = _wrappers.result_wrapper(many_result_func_success)(test_args)

    assert res == new_func_result

def test_result_wrapper_for_zero_params_failure():
    def zero_result_func_failure() -> result.ResultE[str]:
        return result.Result.from_failure(ValueError("test"))
    
    with pytest.raises(ValueError):
        _wrappers.result_wrapper(zero_result_func_failure)()

    with pytest.raises(ValueError):
        raise zero_result_func_failure()._inner_value


@pytest.mark.parametrize("test_args", [1, [1,2], [1,2,3], [1,2,3,4]])
def test_result_wrapper_for_many_params_failure(test_args):
    def many_result_func_failure(*args) -> result.ResultE[Any]:
        return result.Result.from_failure(ValueError(args))

    with pytest.raises(ValueError):
        _wrappers.result_wrapper(many_result_func_failure)(test_args)
    
    with pytest.raises(ValueError):
        raise many_result_func_failure(test_args)._inner_value


def test_io_result_wrapper_for_zero_params_success():
    def zero_io_result_func_success() -> io.IOResultE[str]:
        return io.IOSuccess.from_value("test")
    
    result = zero_io_result_func_success()._inner_value._inner_value

    new_func_result = _wrappers.io_result_wrapper(zero_io_result_func_success)()

    assert result == new_func_result

@pytest.mark.parametrize("test_args", [1, [1, 2], [1,2,3], [1,2,3,4]])
def test_io_result_wrapper_for_many_params_success(test_args):
    def many_io_result_func_success(*args) -> io.IOResultE[Any]:
        return io.IOSuccess.from_value(args)
    
    result = many_io_result_func_success(test_args)._inner_value._inner_value

    new_func_result = _wrappers.io_result_wrapper(many_io_result_func_success)(test_args)

    assert result == new_func_result

def test_io_result_wrapper_for_zero_params_failure():
    def zero_io_result_func_failure() -> io.IOResultE[str]:
        return io.IOFailure(ValueError("test"))
    
    with pytest.raises(ValueError):
        _wrappers.io_result_wrapper(zero_io_result_func_failure)()
    
    with pytest.raises(ValueError):
        raise zero_io_result_func_failure()._inner_value._inner_value

@pytest.mark.parametrize("test_args", [1, [1,2], [1,2,3], [1,2,3,4]])
def test_io_result_wrapper_for_many_params_failure(test_args):
    def many_io_result_func_failure(*args) -> io.IOResultE[str]:
        return io.IOFailure(ValueError(args))
    
    with pytest.raises(ValueError):
        _wrappers.io_result_wrapper(many_io_result_func_failure)(test_args)
    
    with pytest.raises(ValueError):
        raise many_io_result_func_failure(test_args)._inner_value._inner_value
