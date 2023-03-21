import os
import socket
import subprocess
from xmlrpc.client import Boolean

from appium.webdriver.appium_service import AppiumService, AppiumServiceError

from config import LOG_DIR


def appium_start(host: str, port: int, log_name: str):
    try:
        service = AppiumService()
        if not service.is_running:
            service.start(
                stdout=open(f'{LOG_DIR}/{log_name}.log', 'w', encoding='utf8'),
                stderr=subprocess.STDOUT,
                timeout_ms=3000,
                args=[
                    '--address',
                    host,
                    '-p',
                    str(port),
                    '--base-path',
                    '/wd/hub',
                ],
            )
    except AppiumServiceError as error:
        print(error)


def check_port(host, port: int) -> Boolean:
    '''
    確認 port 是否有被佔用
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        s.shutdown(2)
    except OSError:
        print(f'port {port} is available! ')
        return True
    else:
        print(f'port {port} already be in use !')
        return False


def release_port(port: int):
    '''
    釋放 port
    '''
    cmd_find = f'netstat -aon | grep {port}'
    result = os.popen(cmd_find).read()

    if str(port) and 'LISTENING' in result:
        i = result.index('LISTENING')
        start = i + len('LISTENING') + 7
        end = result.index('\n')
        pid = result[start:end]
        cmd_kill = f'taskkill -f -pid {pid}'
        os.popen(cmd_kill)
    else:
        print(f'port {port} is available !')


if __name__ == '__main__':
    appium_start('127.0.0.1', 4723, 'test_start_server.txt')
