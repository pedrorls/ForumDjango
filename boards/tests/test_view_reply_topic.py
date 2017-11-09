from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from ..models import *
from ..views import reply_topic
from ..forms import PostForm


class ReplyTopicsTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.username = 'Pedro'
        self.password = 'senha123'
        user = User.objects.create_user(username=self.username, password=self.password, email='pedro@example.com')
        self.topic = Topic.objects.create(subject='Hello, Django !', board=self.board, starter=user)
        Post.objects.create(message='Its an example of a simple post', topic=self.topic, created_by=user)
        self.url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})


class LoginRequiredReplyTopicTests(ReplyTopicsTestCase):

    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{0}?next={1}'.format(login_url, self.url))

    def test_user_is_autheticated(self):
        self.client.login(username='Pedro', password='senha123')
        response = self.client.get(reverse('home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class ReplyTopicTests(ReplyTopicsTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username='Pedro', password='senha123')

    def test_reply_topic_status_code(self):        
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_reply_invalid_topic_status_code(self):
        url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_reply_view_resolves_reply_topic_view(self):
        view = resolve('/boards/1/topics/1/reply/')
        self.assertEquals(view.func, reply_topic)

    def test_reply_view_shows_form(self):
        response = self.client.get(self.url)
        form = response.context.get('form')
        self.assertIsInstance(form, PostForm)

    def test_reply_view_form_csrf(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_reply_view_form_inputs(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<input', 1)


class SuccessfulReplyTopicTests(ReplyTopicsTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username='Pedro', password='senha123')

    def test_new_reply_valid_post_data(self):
        data = {
            'message': 'Nothing relevant to say here'
        }
        response = self.client.post(self.url, data)
        self.assertTrue(Topic.objects.exists())

    def test_reply_redirect_after_valid_reply(self):
        data = {
            'message': 'Nothing relevant to say here'
        }
        response = self.client.post(self.url, data)
        url = reverse('topic_posts', kwargs={'pk': self.topic.board.pk ,'topic_pk': self.topic.pk})
        topic_posts_url = '{url}?page=1#2'.format(url=url)
        self.assertRedirects(response, topic_posts_url)


class InvalidReplyTopicTests(ReplyTopicsTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username='Pedro', password='senha123')


    def test_new_reply_invalid_empty_post_data(self):
        response = self.client.post(self.url, {})
        form = response.context.get('form')
        self.assertTrue(form.errors)

    def test_invalid_new_reply_does_not_create_object(self):
        old = Topic.objects.count()
        self.client.post(self.url, {})
        new = Topic.objects.count()  
        self.assertEqual(old, new)
