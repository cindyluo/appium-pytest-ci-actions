import pytest

from config import API_HOST, SCREENSHOTS_DIR, CalculatorElements
from appium.webdriver.webdriver import WebDriver
from utils.driver_helper import Base


@pytest.mark.skip_by_env('staging')
def test_production_host():
    assert API_HOST == "https://api.test.com"


class TestCalculator(object):
    @pytest.mark.skip_by_platform('ios')
    def test_android_calculator(self, common_driver: WebDriver):
        driver = common_driver
        base = Base(driver)

        for num in range(1, 11):
            if num < 10:
                button_digit_element = (
                    CalculatorElements.BUTTON_DIGIT_PREFIX[0],
                    f'{CalculatorElements.BUTTON_DIGIT_PREFIX[1]}_{num}',
                )
                _, button_digit = base.find_element(button_digit_element)
                button_digit.click()
            else:
                for char in str(num):
                    button_digit_element = (
                        CalculatorElements.BUTTON_DIGIT_PREFIX[0],
                        f'{CalculatorElements.BUTTON_DIGIT_PREFIX[1]}_{char}',
                    )
                    _, button_digit = base.find_element(button_digit_element)
                    button_digit.click()

            _, button_op_add = base.find_element(CalculatorElements.BUTTON_OP_ADD)
            button_op_add.click()

        _, button_eq = base.find_element(CalculatorElements.BUTTON_EQ)
        button_eq.click()

        _, text_result = base.find_element(CalculatorElements.TEXT_RESULT)
        assert text_result.text == "55"

    # @pytest.mark.skip_by_platform('android')
    # def test_ios_landing(self, common_driver: WebDriver):
