from django.utils.html import escape
from django.test import TestCase
from django.contrib.auth import get_user_model
from lists.models import Item, List
from lists.forms import (
    ItemForm,
    EMPTY_ITEM_ERROR,
    DUPLICATE_ITEM_ERROR,
    ExistingListItemForm,
)

from lxml import html

User = get_user_model()


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):

        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_home_page_users_item_form(self):
        response = self.client.get("/")
        self.assertIsInstance(response.context["form"], ItemForm)

    def test_renders_input_form(self):
        mylist = List.objects.create()
        url = f"/lists/{mylist.id}/"
        response = self.client.get(url)

        parsed = html.fromstring(response.content)
        forms = parsed.cssselect("form[method=POST]")
        self.assertIn(url, [form.get("action") for form in forms])
        [form] = [form for form in forms if form.get("action") == url]

        inputs = form.cssselect("input")
        self.assertIn("text", [input.get("name") for input in inputs])


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="other list item", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "other list item")

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/",
            data={"text": "A new item for an existing list"},
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/",
            data={"text": "A new list item"},
        )
        self.assertRedirects(response, f"/lists/{correct_list.id}/")

    def post_invalid_input(self):
        mylist = List.objects.create()
        return self.client.post(f"/lists/{mylist.id}/", data={"text": ""})

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list.html")

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context["form"], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_displays_item_form(self):
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        self.assertIsInstance(response.context["form"], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        Item.objects.create(list=list1, text="textey")
        response = self.client.post(
            f"/lists/{list1.id}/",
            data={"text": "textey"},
        )

        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, "list.html")
        self.assertEqual(Item.objects.all().count(), 1)


class NewListTest(TestCase):

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertIsInstance(response.context["form"], ItemForm)
        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(List.objects.count(), 0)


class MyListsTest(TestCase):
    def test_my_lists_url_renders_my_lists_template(self):
        User.objects.create(email="a@b.com")
        response = self.client.get("/lists/users/a@b.com/")
        self.assertTemplateUsed(response, "my_lists.html")

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email="wrong@owner.com")
        correct_user = User.objects.create(email="a@b.com")
        response = self.client.get("/lists/users/a@b.com/")

        self.assertEqual(
            response.context["owner"],
            correct_user,
        )

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        user = User.objects.create(email="a@b.com")
        self.client.force_login(user)

        self.client.post("/lists/new", data={"text": "new item"},)
        new_list = List.objects.get()

        self.assertEqual(new_list.owner, user)
