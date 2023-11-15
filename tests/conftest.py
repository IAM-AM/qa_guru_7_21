import pytest
import os
import allure
import allure_commons

from appium.options.ios import XCUITestOptions
from appium.options.android import UiAutomator2Options
from appium import webdriver
from selene import browser, support
from dotenv import load_dotenv

from config import config
import utils


@pytest.fixture(scope='session', autouse=True)
def load_end():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def mobile_management(request):
    user_name = os.getenv('userName')
    access_key = os.getenv('accessKey')

    if request.param == 'Android':
        options = UiAutomator2Options().load_capabilities({
            "platformName": "android",
            "platformVersion": "12.0",
            "deviceName": "Samsung Galaxy S22 Ultra",

            "app": config.app_id,

            'bstack:options': {
                "projectName": "First Python project",
                "buildName": "browserstack-build-1",
                "sessionName": "BStack first_test",

                "userName": user_name,
                "accessKey": access_key
            }
        })
    else:
        options = XCUITestOptions().load_capabilities({
            "platformName": "ios",
            "platformVersion": "17",
            "deviceName": "iPhone 12",

            "app": config.app_id,

            "bstack:options": {
                "projectName": "First Python project",
                "buildName": "browserstack-build-1",
                "sessionName": "BStack first_test",

                "userName": user_name,
                "accessKey": access_key,
            }
        })
    with allure.step('Init app session'):
        browser.config.driver = webdriver.Remote(
            config.browser_url,
            options=options
        )

    browser.config.timeout = config.timeout

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield browser

    utils.add_screenshot(browser)
    utils.add_xml(browser)

    session_id = browser.driver.session_id

    with allure.step('Tear down app session'):
        browser.quit()

    utils.attach_bstack_video(session_id, user_name, access_key)


ios = pytest.mark.parametrize('mobile_management', ['IOS'], indirect=True)
android = pytest.mark.parametrize('mobile_management', ['Android'], indirect=True)
