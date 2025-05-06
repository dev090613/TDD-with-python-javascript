from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import unittest
import time


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_todo_list(self):

        # Edith는 멋진 to-do app을 알게 되었다.
        # 그녀는 홈페이지에 방문한다.
        self.browser.get("http://localhost:8000")

        # 그녀는 홈페이지 title과 header이
        # "To-Do"로 시작함을 확인
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # 그녀는 to-do 항목을 입력할 수 있도록 초대 받음
        # placeholder를 확인(<input placeholder="..">)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # 그녀는 "Buy peacock feathers"를 텍스트 박스에 입력
        inputbox.send_keys("Buy peacock feathers")
        # 엔터를 누르면, 페이지가 업데이트 되고,
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        # "1: Buy peacock feathers"라는 항목이 to-do 리스트에
        self.assertTrue(
            any(row.text == "1: Buy peacock feathers" for row in rows),
            "New to-do item did not appear in table",
        )


        self.fail("Finish the test!")


# 여전히 다른 항목을 입력할 수 있음
# "Use peacock feathers to make a fly" 입력 & 엔터

# 페이지가 다시 업데이트되고, 리스트에는 두 개의 항목

# 그녀는 자러 간다

if __name__ == "__main__":
    unittest.main()
