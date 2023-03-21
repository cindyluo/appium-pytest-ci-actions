import os

import click
import pytest

from config import ALLURE_RESULTS_DIR, SERVER_HOST, SERVER_PORT


@click.command()
@click.option('-d', '--device_name', 'device_name', type=str, required=True)
def run_tests(device_name):
    device_info = {
        'device_name': device_name,
        'server_host': SERVER_HOST,
        'server_port': SERVER_PORT,
    }

    pytest.main(['--cmdopt={}'.format(device_info), '--alluredir', ALLURE_RESULTS_DIR, '-vs'])


if __name__ == '__main__':
    run_tests()
