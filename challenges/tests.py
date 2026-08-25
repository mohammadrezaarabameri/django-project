from unittest.mock import patch

from django.http import Http404, HttpResponse
from django.test import RequestFactory, SimpleTestCase, TestCase

from WebDjango.asgi import application as asgi_application
from WebDjango.views import index
from WebDjango.wsgi import application as wsgi_application
from challenges import views


class ProjectViewsTests(SimpleTestCase):
    def test_index_returns_greeting(self):
        response = index(RequestFactory().get('/'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b"Hello, world. You're at the polls index.",
        )


class ChallengesViewsTests(SimpleTestCase):
    def setUp(self):
        self.request = RequestFactory().get('/user/')

    def test_profile_returns_profile_response(self):
        response = views.profile(self.request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'user profile')

    def test_edit_returns_edit_response(self):
        response = views.edit(self.request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'user edit')

    @patch('challenges.views.render')
    def test_dynamic_users_renders_known_user(self, render):
        render.return_value = HttpResponse()

        response = views.dynamic_users(self.request, 2)

        self.assertIs(response, render.return_value)
        render.assert_called_once_with(
            self.request,
            'challenges/challenge.html',
            {'data': 'user two', 'user': 2},
        )

    def test_dynamic_users_raises_404_for_unknown_user(self):
        with self.assertRaises(Http404):
            views.dynamic_users(self.request, 99)

    @patch('challenges.views.render')
    def test_list_users_renders_all_user_ids(self, render):
        render.return_value = HttpResponse()

        response = views.list_users(self.request)

        self.assertIs(response, render.return_value)
        render.assert_called_once_with(
            self.request,
            'challenges/index.html',
            {'users': [1, 2, 3, 4]},
        )


class DynamicUsersViewTests(TestCase):
    def test_known_user_is_rendered(self):
        response = self.client.get('/user/1')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user own')

    def test_unknown_user_returns_404(self):
        with self.assertLogs('challenges.views', level='WARNING') as logs:
            response = self.client.get('/user/99')

        self.assertEqual(response.status_code, 404)
        self.assertIn('Requested unknown user id 99', logs.output[0])


class ListUsersViewTests(TestCase):
    def test_lists_every_user(self):
        response = self.client.get('/user/')

        self.assertEqual(response.status_code, 200)
        for user_id in (1, 2, 3, 4):
            self.assertContains(response, f'/user/{user_id}')


class DeploymentApplicationsTests(SimpleTestCase):
    def test_asgi_application_is_callable(self):
        self.assertTrue(callable(asgi_application))

    def test_wsgi_application_is_callable(self):
        self.assertTrue(callable(wsgi_application))
