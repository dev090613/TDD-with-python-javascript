from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 5


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        self.fail("Write me!")
