import time

import pytest

from config import ENV, PLATFORM
from utils.appium_helper import release_port
from utils.driver_helper import BaseDriver

base_driver = None


def pytest_addoption(parser):
    parser.addoption("--cmdopt", action="store", default="device_info", help=None)


@pytest.fixture
def env():
    return ENV


@pytest.fixture
def platform():
    return PLATFORM


@pytest.fixture(autouse=True)
def skip_by_env(request, env):
    if request.node.get_closest_marker('skip_by_env'):
        if request.node.get_closest_marker('skip_by_env').args[0] == env:
            pytest.skip(f'skipped on this env: {env}')


@pytest.fixture(autouse=True)
def skip_by_platform(request, platform):
    if request.node.get_closest_marker('skip_by_platform'):
        if request.node.get_closest_marker('skip_by_platform').args[0] == platform:
            pytest.skip(f'skipped on this platform: {platform}')


def pytest_configure(config):
    config.addinivalue_line('markers', 'skip_by_env(env): skip test for the given environment')
    config.addinivalue_line(
        'markers',
        'skip_by_platform(platform): skip test for the given search engine',
    )


@pytest.fixture(scope="session")
def cmd_opt(request):
    return request.config.getoption("--cmdopt")


@pytest.fixture(scope="session")
def common_driver(cmd_opt):
    cmd_opt = eval(cmd_opt)
    print("cmd_opt", cmd_opt)
    global base_driver
    base_driver = BaseDriver(cmd_opt)
    time.sleep(1)
    driver = base_driver.get_base_driver()
    yield driver
    driver.quit()
    release_port(cmd_opt["server_port"])
