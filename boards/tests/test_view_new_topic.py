from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.urls import resolve
from django.test import TestCase
from ..models import *
from ..views import new_topic
from ..forms import NewTopicForm

# class NewTopicTests(TestCase):
#     def setUp(self):
#         Board.objects.create(name='Django', description='Django board.')
#         User.objects.create_user(username='Pedro', email='pedro@example.com', password='senha123')

#     def url_reverse(self, url_name, pk):
#         url = reverse(url_name, kwargs={'pk': pk})
#         return url

#     def test_new_topic_view_success_status_code(self):
#         url = self.url_reverse('new_topic', 1)
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 200)

#     def test_new_topic_view_not_found_status_code(self):
#         url = self.url_reverse('new_topic', 99)
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 404)

#     def test_new_topic_view_resolves_new_topic_view(self):
#         view = resolve('/boards/1/new/')
#         self.assertEquals(view.func, new_topic)

#     def test_new_topic_view_contains_link_back_to_boards_topics_view(self):
#         new_topic_url = self.url_reverse('new_topic', 1)
#         board_topics_url = self.url_reverse('board_topics', 1)
#         response = self.client.get(new_topic_url)
#         self.assertContains(response, 'href="{0}"'.format(board_topics_url))

#     def test_csrf(self):
#         url = self.url_reverse('new_topic', 1)
#         response = self.client.get(url)
#         self.assertContains(response, 'csrfmiddlewaretoken')

#     def test_new_topic_valid_post_data(self):
#         url = self.url_reverse('new_topic', 1)
#         data = {
#             'subject': 'Test title',
#             'message': 'Lorem ipsum dolor sit amet'
#         }
#         response = self.client.post(url, data)
#         self.assertTrue(Topic.objects.exists())
#         self.assertTrue(Post.objects.exists())

#     def test_new_topic_invalid_post_data(self):
#         url = self.url_reverse('new_topic', 1)
#         response = self.client.post(url, {})
#         self.assertEquals(response.status_code, 200)

#     def test_new_topic_invalid_post_data_empty_fields(self):
#         url = self.url_reverse('new_topic', 1)
#         data = {
#             'subject': '',
#             'message': '',
#         }
#         response = self.client.post(url, data)
#         self.assertEquals(response.status_code, 200)
#         self.assertFalse(Topic.objects.exists())
#         self.assertFalse(Post.objects.exists())

#     def test_contains_form(self):
#         url = self.url_reverse('new_topic', 1)
#         response = self.client.get(url)
#         form = response.context.get('form')
#         self.assertIsInstance(form, NewTopicForm)

#     def test_new_topic_invalid_post_data(self):
#         url = self.url_reverse('new_topic', 1)
#         response = self.client.post(url, {})
#         form = response.context.get('form')
#         self.assertEquals(response.status_code, 200)
#         self.assertTrue(form.errors)


class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        self.url = reverse('new_topic', kwargs={'pk': 1})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{0}?next={1}'.format(login_url, self.url))
        