from appium.webdriver.common.appiumby import AppiumBy


class CalculatorElements:
    BUTTON_DIGIT_PREFIX = (AppiumBy.ID, 'com.google.android.calculator:id/digit')
    BUTTON_OP_ADD = (AppiumBy.ID, 'com.google.android.calculator:id/op_add')
    BUTTON_EQ = (AppiumBy.ID, 'com.google.android.calculator:id/eq')

    TEXT_RESULT = (AppiumBy.ID, 'com.google.android.calculator:id/result_final')
