from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Specialty, Schedule, Doctors
from .forms import UserForm
from datetime import datetime as dt


'''Models'''


class SpecialtyModelTestCase(TestCase):
    def setUp(self):
        self.title = 'Терапевт'
        Specialty.objects.create(title=self.title)

    def test_specialty_model(self):
        obj = Specialty.objects.get(title=self.title)
        self.assertEqual(obj.title, 'Терапевт')


class DoctorsModelTestCase(TestCase):
    def setUp(self):
        self.title = 'Терапевт'
        self.spec = Specialty.objects.create(title=self.title)
        self.full_name = 'Трушин В.М.'
        Doctors.objects.create(specialty_id=self.spec.pk, full_name=self.full_name)

    def test_doctors_model(self):
        obj = Doctors.objects.get(full_name=self.full_name)
        self.assertEqual(obj.full_name, 'Трушин В.М.')


class ScheduleModelTestCase(TestCase):
    def setUp(self):
        self.title = 'Терапевт'
        self.spec = Specialty.objects.create(title=self.title)
        self.full_name = 'Трушин В.М.'
        self.doc = Doctors.objects.create(specialty_id=self.spec.pk, full_name=self.full_name)
        self.client = 'Федр Федоров'
        self.pub_date = dt(2017, 9, 8)
        Schedule.objects.create(specialty_id=self.spec.pk, doctor_id=self.doc.pk, client=self.client, pub_date=self.pub_date)

    def test_schedule_model(self):
        obj = Schedule.objects.get(pub_date=dt(2017, 9, 8))
        self.assertEqual(obj.client, 'Федр Федоров')


'''Forms'''


class UserFormTestCase(TestCase):
    def setUp(self):
        username = 'petrov'
        password = '135adg'
        first_name = 'Petr'
        last_name = 'Petrov'
        email = 'piton@mail.com'
        self.data = {'username': username, 'password': password, 'first_name': first_name, 'email': email,
                'last_name': last_name}

    def test_valid_form(self):
        form = UserForm(data=self.data)
        self.assertTrue(form.is_valid())


class UserAuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_auth_user(self):
        response = self.client.post('/', {'username': 'ivanov', 'password': '190683andrey'})
        self.assertTrue(response)


class DoctorsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_doctors_redirect_to_login_view(self):
        response = self.client.post('/doctors/', {})
        self.assertRedirects(response, '/')

    def test_doctors_view(self):
        user = User.objects.create_user(username='petrov', email='piton@mail.com', password='135adg')
        log_in = self.client.post('/', username=user.username, password=user.password, email='piton@mail.com')
        print('log_in =', log_in)
        self.assertTrue(log_in)