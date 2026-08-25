from django.test import TestCase


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
