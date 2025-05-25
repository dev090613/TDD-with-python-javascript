from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 5


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):

        self.browser.get(self.live_server_url)
        # 빈 항목 제출
        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)

        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").text,
                "You can't have an empty list item",
            )
        )

        return # early return

        self.browser.find_element(By.ID, "id_new_item").send_keys("Purchase milk")
        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Purchase milk")

        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").text,
                "You can't have an empty list item",
            )
        )

        self.browser.find_element(By.ID, "id_new_item").send_keys("Make tea")
        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("2: Make tea")
