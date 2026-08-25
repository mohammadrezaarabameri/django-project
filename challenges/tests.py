from unittest.mock import patch

from django.http import Http404, HttpResponse
from django.test import RequestFactory, SimpleTestCase

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


class DeploymentApplicationsTests(SimpleTestCase):
    def test_asgi_application_is_callable(self):
        self.assertTrue(callable(asgi_application))

    def test_wsgi_application_is_callable(self):
        self.assertTrue(callable(wsgi_application))
