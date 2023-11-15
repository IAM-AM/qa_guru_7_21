import allure

from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have
from tests.conftest import ios


@ios
def test_text_input():
    with allure.step('Enter email'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Text Button')).click()
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Text Input')).type('mail@example.com').press_enter()

    with allure.step('Check email'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Text Output')).should(have.text('mail@example.com'))
