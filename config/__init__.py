import os
from pathlib import Path

from ppadb.client import Client as AdbClient

ROOT_DIR = Path().resolve()
ENV = os.environ.get('ENV')
PLATFORM = os.environ.get('PLATFORM')
SERVER_HOST = os.environ.get('SERVER_HOST', '127.0.0.1')
SERVER_PORT = os.environ.get('SERVER_PORT', '4723')
DEVICE_NAME = os.environ.get('DEVICE_NAME')

if ENV == 'production':
    from config.production import *
else:
    from config.staging import *

if PLATFORM == 'android':
    from config.elements_android import *
else:
    from config.elements_ios import *

ANDROID_APP_ACTIVITY = 'com.android.calculator2.Calculator'
ANDROID_APP_PACKAGE = 'com.google.android.calculator'

DEVICES = {}
client = AdbClient(host='127.0.0.1', port=5037)
for device in client.devices():
    DEVICES[device.serial] = {
        'platformName': 'Android',
        'automationName': 'UiAutomator2',
        'platformVersion': device.shell('getprop ro.build.version.release').replace('\n', ''),
        'language': 'en',
        'locale': 'US',
        'deviceName': device.serial,
        'appActivity': ANDROID_APP_ACTIVITY,
        'appPackage': ANDROID_APP_PACKAGE,
        'app': str(Path(ROOT_DIR, 'apk', 'calculator.apk')),
        'noReset': True,
        'udid': device.serial,
    }

LOG_DIR = Path(ROOT_DIR, 'log')
LOG_DIR.mkdir(parents=True, exist_ok=True)

SCREENSHOTS_DIR = Path(ROOT_DIR, 'screenshots')
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

ALLURE_RESULTS_DIR = Path(ROOT_DIR, 'allure-results')
ALLURE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
