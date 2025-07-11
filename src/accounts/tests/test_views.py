from unittest import mock
from django.test import TestCase
from django.contrib import auth
from accounts.models import Token


class SendLoginEmailViewTest(TestCase):
    def test_redirects_to_home_page(self):
        response = self.client.post(
            "/accounts/send_login_email",
            data={"email": "edith@example.com"},
        )
        self.assertRedirects(response, "/")

    @mock.patch("accounts.views.send_mail")
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        self.client.post(
            "/accounts/send_login_email",
            data={"email": "edith@example.com"},
        )
        self.assertEqual(mock_send_mail.called, True)

        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, "Your login link for Superlists")
        self.assertEqual(from_email, "noreply@superlists")
        self.assertEqual(to_list, ["edith@example.com"])

    def test_adds_success_message(self):
        response = self.client.post(
            "/accounts/send_login_email",
            data={"email": "edith@example.com"},
            follow=True,
        )

        message = list(response.context["messages"])[0]
        self.assertEqual(
            message.message,
            "Check your email, we've sent you a link you can use to log in.",
        )
        self.assertEqual(message.tags, "success")

    def test_creates_token_associated_with_email(self):
        self.client.post(
            "/accounts/send_login_email",
            data={"email": "edith@example.com"},
        )
        token = Token.objects.get()
        self.assertEqual(token.email, "edith@example.com")

    @mock.patch("accounts.views.send_mail")
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        self.client.post(
            "/accounts/send_login_email",
            data={"email": "edith@example.com"},
        )

        token = Token.objects.get()
        expected_url = f"http://testserver/accounts/login?token={token.uid}"

        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)


class LoginViewTest(TestCase):
    def test_redirects_to_home_page(self):
        response = self.client.get("/accounts/login?token=abcd123")
        self.assertRedirects(response, "/")

    def test_logs_in_if_given_valid_token(self):

        anon_user = auth.get_user(self.client)
        self.assertEqual(anon_user.is_authenticated, False)

        token = Token.objects.create(email="edith@example.com")
        self.client.get(f"/accounts/login?token={token.uid}")

        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(user.email, "edith@example.com")

    def test_shows_login_error_if_token_invalid(self):
        response = self.client.get("/accounts/login?token=invalid-token", follow=True)
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)

        message = list(response.context["messages"])[0]
        self.assertEqual(
            message.message,
            "Invalid login link, please request a new one",
        )
        self.assertEqual(message.tags, "error")

    @mock.patch("accounts.views.auth")
    def test_calls_django_auth_authenticate(self, mock_auth):
        self.client.get("/accounts/login?token=abc123")
        self.assertEqual(
            mock_auth.authenticate.call_args,
            mock.call(uid="abc123"),
        )
