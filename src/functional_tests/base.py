import os
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from .container_commands import reset_database


MAX_WAIT = 5


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.test_server = os.environ.get("TEST_SERVER")
        if self.test_server:
            self.live_server_url = "http://" + self.test_server
            reset_database(self.test_server)

    def tearDown(self):
        self.browser.quit()

    def wait(fn):
        def modifed_fn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep(0.5)

        return modifed_fn

    @wait
    def wait_for_row_in_list_table(self, row_text):
        rows = self.browser.find_elements(By.CSS_SELECTOR, "#id_list_table tr")
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element(By.CSS_SELECTOR, "#id_logout")
        navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element(By.CSS_SELECTOR, "input[name=email]")
        navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        self.assertNotIn(email, navbar.text)

    @wait
    def wait_for(self, fn):
        return fn()

    def get_item_input_box(self):
        return self.browser.find_element(By.ID, "id_text")

    def add_list_item(self, item_text):
        num_rows = len(
            self.browser.find_elements(
                By.CSS_SELECTOR,
                "#id_list_table tr",
            ),
        )

        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f"{item_number}: {item_text}")
