import pytest
from logger import Logger
import datetime


@pytest.fixture(scope="function", autouse=True)
def step_start_time(request):
    Logger.log.info(f"Starting test: {request.node.name} - {datetime.datetime.now()}")
    yield
    Logger.log.info(f"Finished test: {request.node.name} - {datetime.datetime.now()}")
