from typing import Dict, Tuple

from appium import webdriver
from appium.webdriver import WebElement
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from config import DEVICES
from utils.appium_helper import appium_start, check_port, release_port


class BaseDriver(object):
    '''
    Get Device
    '''

    def __init__(self, device_info: Dict[str, int]):
        self.device_info = device_info
        self.device_name = self.device_info['device_name']
        self.host = self.device_info['server_host']
        self.port = int(self.device_info['server_port'])
        self.data = DEVICES

        if not check_port(self.host, self.port):
            release_port(self.port)
        appium_start(self.host, self.port, self.device_name)

    def get_base_driver(self):
        caps = self.data[self.device_name]
        driver = webdriver.Remote(
            command_executor='http://' + self.host + ':' + str(self.port) + '/wd/hub',
            desired_capabilities=caps,
        )
        print(f'=====driver:{driver}=======')
        return driver


class Base(object):
    def __init__(self, driver: WebDriver):
        self.driver = driver

    @property
    def get_phone_size(self):
        """取得螢幕的大小"""
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']
        print(f'phone_size: width is {width} and height is {height}')
        return width, height

    def swipe_left(self, element: WebElement = None):
        """左滑"""
        actions = TouchAction(self.driver)
        width, height = self.get_phone_size
        start = width * 0.9, height * 0.5
        end = width * 0.1, height * 0.5
        print(f'start: {start}, end: {end}')
        return actions.long_press(element, *start).move_to(element, *end).release().perform()

    def swipe_right(self, element: WebElement = None):
        """右滑"""
        actions = TouchAction(self.driver)
        width, height = self.get_phone_size
        start = width * 0.1, height * 0.5
        end = width * 0.9, height * 0.5
        print(f'start: {start}, end: {end}')
        return actions.long_press(element, *start).move_to(element, *end).release().perform()

    def swipe_up(self, element: WebElement = None) -> TouchAction:
        """上滑"""
        actions = TouchAction(self.driver)
        width, height = self.get_phone_size
        start = width * 0.5, height * 0.8
        end = width * 0.5, height * 0.2
        print(f'start: {start}, end: {end}')
        return actions.long_press(element, *start).move_to(element, *end).release().perform()

    def swipe_down(self, element: WebElement = None) -> TouchAction:
        """下滑"""
        actions = TouchAction(self.driver)
        width, height = self.get_phone_size
        start = width * 0.5, height * 0.2
        end = width * 0.5, height * 0.8
        print(f'start: {start}, end: {end}')
        return actions.long_press(element, *start).move_to(element, *end).release().perform()

    def find_element(self, locator: tuple, timeout=30) -> Tuple[bool, WebElement]:
        wait = WebDriverWait(self.driver, timeout)
        try:
            element = wait.until(lambda driver: driver.find_element(*locator))
            return True, element
        except (NoSuchElementException, TimeoutException):
            print(f'no found element {locator[1]} by {locator[0]}')
            return False, None


if __name__ == '__main__':
    base = BaseDriver(
        {
            'title': 'Emulator_two',
            'server_host': '127.0.0.1',
            'server_port': 4725,
        }
    )
