from django.test import TestCase, Client
from .forms import UserForm


class UserFormTestCase(TestCase):
    def test_valid_form(self):
        username = 'petrov'
        password = '135adg'
        first_name = 'Petr'
        last_name = 'Petrov'
        email = 'piton@mail.com'
        data = {'username': username, 'password': password, 'first_name': first_name, 'email': email, 'last_name': last_name}
        form = UserForm(data=data)
        print(form.errors)
        self.assertTrue(form.is_valid())


class UserAuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_auth_user(self):
        response = self.client.post('/', {'username': 'ivanov', 'password': '190683andrey'})
        print('response =',response)
        self.assertTrue(response)