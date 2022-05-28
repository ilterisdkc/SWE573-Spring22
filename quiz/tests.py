from django.contrib.auth import authenticate
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


# Create your tests here.
class LoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='unittest',
            password='wasd1234',
            email='unit@test.com'
        )
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='unittest', password="wasd1234")
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username="wrong_name", password="wasd1234")
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username="unittest", password="wrong_password")
        self.assertFalse(user is not None and user.is_authenticated)

# TODO: view test will be handled by either using APIClient or finding another solution.
# class SignInViewTest(APITestCase):
#
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username='view',
#             password='wasd1234',
#             email='test@example.com'
#         )
#
#     def tearDown(self):
#         self.user.delete()
#
#     def test_correct(self):
#         data = {"username": "view", "password": "wasd1234"}
#         response = self.client.post('/login/', data)
#         self.assertTrue(response['authenticated'])
#
#     def test_wrong_username(self):
#         data = {"username": "wrong", "password": "wasd1234"}
#         response = self.client.post('/login/', data)
#         self.assertFalse(response['authenticated'])
#
#     def test_wrong_password(self):
#         data = {"username": 'view', "password": "wrong"}
#         response = self.client.post('/login/', data)
#         self.assertFalse(response['authenticated'])
