from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse
from django.test import TestCase


class PasswordResetMailTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='pedro', email='pedro@example.com', password='senha123')
        self.response = self.client.post(reverse('password_reset'), {'email': 'pedro@example.com'})
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual('[Boards] Please reset your password.', self.email.subject)

    def test_email_body(self):
        token = self.response.context.get('token')
        uid = self.response.context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('pedro', self.email.body)
        self.assertIn('pedro@example.com', self.email.body)

    def test_email_to(self):
        self.assertEqual(['pedro@example.com'], self.email.to)