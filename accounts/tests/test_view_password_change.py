from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase


class LoginRequiredPasswordChangeTests(TestCase):
    def test_redirection_to_login(self):
        url = reverse('password_change')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')


class PasswordChangeTestCase(TestCase):
    def setUp(self, data={}):
        self.user = User.objects.create_user(username='pedro', password='senha123', email='pedro@example.com')
        self.url = reverse('password_change')
        self.client.login(username='pedro', password='senha123')
        self.response = self.client.post(self.url, data)


class SuccessfulPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self):
        super().setUp({
            'old_password': 'senha123',
            'new_password1': '123senha',
            'new_password2': '123senha',
        })
        
    def test_password_change_redirection(self):
        self.assertRedirects(self.response, reverse('password_change_done'))

    def test_password_changed(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('123senha'))

    def test_if_user_is_authenticated(self):
        response = self.client.get(reverse('home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidPasswordChangeTests(PasswordChangeTestCase):
    def test_invalid_password_change_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_check_invalid_password_change_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_if_password_did_not_change(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('senha123'))