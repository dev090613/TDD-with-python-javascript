from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_todo_list(self):

        # Edith는 멋진 to-do app을 알게 되었다.
        # 그녀는 홈페이지에 방문한다.
        self.browser.get("localhost:8000")

        # 그녀는 홈페이지 제목이 "To-Do"로 시작함을 확인
        self.assertIn("To-Do", self.browser.title)

        # 그녀는 to-do 항목을 입력할 수 있도록 초대 받음
        self.fail("Finish the test!")


# 그녀는 "Buy peacock feathers"를 텍스트 박스에 입력

# 엔터를 누르면, 페이지가 업데이트 되고, 
# "1: Buy peacock feathers"라는 항목이 to-do 리스트에

# 여전히 다른 항목을 입력할 수 있음
# "Use peacock feathers to make a fly" 입력 & 엔터

# 페이지가 다시 업데이트되고, 리스트에는 두 개의 항목

# 그녀는 자러 간다

if __name__ == "__main__":
    unittest.main()
