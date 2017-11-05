from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import views as auth_views
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.urlresolvers import reverse
from django.core import mail
from django.urls import resolve
from django.test import TestCase


class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/reset/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)

    def test_reset_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_reset_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_reset_form_inputs(self):
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)


class SucessfulPasswordResetTests(TestCase):
    def setUp(self):
        email = 'rodrigues@example.com'
        User.objects.create_user(username='Pedro', email=email, password='senha123')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})

    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response,  url)

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': 'donotexist@email.com'})

    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_no_reset_email_sent(self):
        self.assertEqual(0, len(mail.outbox))


class DonePasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_done')
        self.respose = self.client.get(url)

    def test_done_reset_status_code(self):
        self.assertEquals(self.respose.status_code, 200)

    def test_done_reset_view_function(self):
        view = resolve('/reset/done/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetDoneView)


class ConfirmPasswordResetTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='pedro', password='senha123', email='pedro@example.com')
        self.uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        self.token = default_token_generator.make_token(user)
        url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(url, follow=True)

    def test_confirm_reset_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_confirm_reset_view_function(self):
        view = resolve('/reset/{uidb64}/{token}/'.format(
            uidb64=self.uid,
            token=self.token
            ))
        self.assertEquals(view.func.view_class, auth_views.PasswordResetConfirmView)
    
    def test_confirm_reset_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_confirm_reset_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    def test_confirm_reset_form_inputs(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password', 2)


class ConfirmInvalidPasswordReset(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='pedro', password='senha123', email='pedro@example.com')
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        token = default_token_generator.make_token(user)

        user.set_password('123senha')
        user.save()

        url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        self.response = self.client.get(url)

    def test_confirm_reset_invalid_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_confirm_reset_invalid_html(self):
        password_reset_url = reverse('password_reset')
        self.assertContains(self.response, 'invalid password reset link')
        self.assertContains(self.response, 'href="{0}"'.format(password_reset_url))