import allure

from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have
from tests.conftest import android


@android
def test_search():
    with allure.step('Type search'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type('Allure')

    with allure.step('Allure article is found'):
        results = browser.all((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title'))
        results.should(have.size_greater_than(0))
        results.first.should(have.text('Allure'))


@android
def test_open_article_page():
    with allure.step('Search'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type('Allure')

    with allure.step('Open article'):
        results = browser.all(
            (AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title')
        )
        results.first.click()

    with allure.step('Verify content in the article'):
        results = browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/view_wiki_error_text'))
        results.should(have.text('An error occurred'))
