import os
from pathlib import Path
import yaml

from appium.webdriver.common.appiumby import AppiumBy

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


DEVICES = {}
DEFAULT_DEVICES_CONFIG = Path(ROOT_DIR, 'config', 'desired_caps.yaml')
if DEFAULT_DEVICES_CONFIG.exists():
    with open(DEFAULT_DEVICES_CONFIG, 'r', encoding='UTF-8') as f:
        DEVICES = yaml.load(f, Loader=yaml.FullLoader)

EXTEND_DEVICES_CONFIG = Path(ROOT_DIR, 'config', 'extend_desired_caps.yaml')
if EXTEND_DEVICES_CONFIG.exists():
    with open(EXTEND_DEVICES_CONFIG, 'r', encoding='UTF-8') as f:
        DEVICES = DEVICES | yaml.load(f, Loader=yaml.FullLoader)

LOG_DIR = Path(ROOT_DIR, 'log')
LOG_DIR.mkdir(parents=True, exist_ok=True)

SCREENSHOTS_DIR = Path(ROOT_DIR, 'screenshots')
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

ALLURE_RESULTS_DIR = Path(ROOT_DIR, 'allure-results')
ALLURE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
