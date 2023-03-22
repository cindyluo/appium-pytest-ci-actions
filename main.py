import pytest

from config import ALLURE_RESULTS_DIR, DEVICES, SERVER_HOST, SERVER_PORT

device_infos = []
for device_name in DEVICES:
    device_infos.append(
        {
            'device_name': device_name,
            'server_host': SERVER_HOST,
            'server_port': SERVER_PORT,
        }
    )


def run_tests():
    pytest.main(['--cmdopt={}'.format(device_infos[0]), '--alluredir', ALLURE_RESULTS_DIR, '-vs'])


if __name__ == '__main__':
    run_tests()
