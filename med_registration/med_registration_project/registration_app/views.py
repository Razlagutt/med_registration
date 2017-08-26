from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from .forms import UserForm
from .models import Doctors, Specialty, Schedule

# Create your views here.


def schedule(request, id=None):
    context = {}
    if request.user.is_authenticated():
        doctor = get_object_or_404(Doctors, id=id)
        #schedule = Schedule.objects.filter(pub_date__)
        context['doctor'] = doctor
        context['btn_state'] = 'Выйти'
        context['url_state'] = '/logout/'
        context['title_page'] = 'Расписание приема посетителей'
        return render(request, 'registration_app/schedule.html', context)
    else:
        return redirect('registration:user_login')


def doctors_list(request):
    context = {}
    if request.user.is_authenticated():
        specialty = Specialty.objects.all().order_by('id')
        doctors = Doctors.objects.all().order_by('specialty')
        context['doctors'] = doctors
        context['specialty'] = specialty
        context['btn_state'] = 'Выйти'
        context['url_state'] = '/logout/'
        context['title_page'] = 'Специалисты клиники'
        return render(request, 'registration_app/doctors_list.html', context)
    return redirect('registration:user_login')


def user_login(request):
    context = {}
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        username = user_form['username'].data
        password = user_form['password'].data
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('registration:doctors'))
            else:
                context['error'] = 'Данный аккаунт не активен.'
        else:
            context['error'] = 'Неверный логин и/или пароль.'
    else:
        user_form = UserForm()
        context['user_form'] = user_form
        context['btn_state'] = 'Регистрация'
        context['url_state'] = '/registration/'
        context['title_page'] = 'Авторизация'

        return render(request, 'registration_app/login.html', context)


def user_register(request):
    context = {}
    if request.method == 'POST':
        user_form = UserForm(request.POST or None)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)

            return HttpResponseRedirect(reverse('registration:doctors'))
        else:
            context['error'] = 'Пользователь с таким логином уже существует.'
    else:
        user_form = UserForm()
        context['user_form'] = user_form
        context['btn_state'] = 'Авторизация'
        context['url_state'] = '/login/'
        context['title_page'] = 'Регистрация'

        return render(request, 'registration_app/register.html', context)


def user_logout(request):
    logout(request)
    return redirect('registration:user_login')