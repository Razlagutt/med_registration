from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from .forms import UserForm
from .models import Doctors, Specialty, Schedule

from calendar import Calendar
from datetime import time, datetime as dt


def get_datetime(args):

    # Блок получающий актуальные даты текущего месяца
    NOW = dt.today()
    dates = Calendar(0).itermonthdates(NOW.year, NOW.month)
    actual_dates = [date for date in dates if not (dt.isoweekday(date) in [6, 7]) and date >= NOW.date()]

    WORK_DATES = []
    WORK_TIME = [time(hour, 0) for hour in range(9, 19)]
    for actual_date in actual_dates:
        for work_hour in WORK_TIME:
            WORK_DATES.append(dt.combine(actual_date, work_hour))

    # Извлекаем из queryset данные date, time. Не понимаю почему, но через for не хочет работать (хотя иногда работает),
    # требует целочисленный индекс у arg
    qs_dates = [dt.combine(dt.date(arg['pub_date']), dt.time(arg['pub_date'])) for arg in args]

    # Получаем список свободных дней и часов для записи к врачу
    [WORK_DATES.remove(work_date) for work_date in WORK_DATES if work_date in qs_dates]

    # Сортируем список рабочих дат по возрастанию
    work_days = sorted({dt.date(work_date) for work_date in WORK_DATES})

    # Создаем словарь дата: [время] свободных для записи к врачу
    DATES_DICT = {}
    time_list = []
    for work_day in work_days:
        for work_date in WORK_DATES:
            if work_day == dt.date(work_date):
                time_list.append(dt.time(work_date).hour)
        DATES_DICT[work_day] = time_list
        time_list = []

    return {'work_dates': work_days, 'dates_dict': DATES_DICT}


def schedule(request, id):
    if request.user.is_authenticated():
        current_date = dt.combine(dt.today().date(), time(0, 0))
        schedule_query = Schedule.objects.filter(doctor__id=id, pub_date__gte=current_date).order_by('pub_date').values()
        datetime_list = get_datetime(schedule_query)
        context = {
            'work_dates': datetime_list['work_dates'],
            'dates_dict': datetime_list['dates_dict'],
            'doctor': get_object_or_404(Doctors, id=id),
            'btn_title': 'Выйти',
            'url_btn': reverse('registration:user_logout'),
            'title_page': 'Расписание приема посетителей',
        }
        return render(request, 'registration_app/schedule.html', context)
    else:
        return redirect('registration:user_login')


def record(request, id, year, month, day, hour):
    if request.user.is_authenticated():
        str_date = '{}/{}/{} {}:00'.format(year, month, day, hour)
        format_str = "%Y/%m/%d %H:%M"
        context = {
            'client': '{} {}'.format(request.user.first_name, request.user.last_name),
            'doctor': get_object_or_404(Doctors, id=id),
            'record_date': dt.strptime(str_date, format_str).date(),
            'record_time': dt.strptime(str_date, format_str).time(),
            'btn_title': 'Выйти',
            'url_btn': reverse('registration:user_logout'),
            'title_page': 'Лист записи',
        }
        record_list = Schedule(client=context['client'],
                          pub_date=dt.combine(context['record_date'], context['record_time']),
                          doctor=context['doctor'],
                          specialty=context['doctor'].specialty
                          )
        record_list.save()
        return render(request, 'registration_app/record.html', context)
    else:
        return redirect('registration:user_login')


def doctors(request):
    if request.user.is_authenticated():
        context = {
            'doctors': Doctors.objects.all().order_by('specialty'),
            'specialty': Specialty.objects.all().order_by('id'),
            'btn_title': 'Выйти',
            'url_btn': reverse('registration:user_logout'),
            'title_page': 'Специалисты клиники',
        }
        return render(request, 'registration_app/doctors.html', context)
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
            user_form = UserForm()
            context['user_form'] = user_form
            context['btn_title'] = 'Регистрация'
            context['url_btn'] = reverse('registration:user_register')
            context['title_page'] = 'Авторизация'
            return render(request, 'registration_app/login.html', context)
    else:
        user_form = UserForm()
        context['user_form'] = user_form
        context['btn_title'] = 'Регистрация'
        context['url_btn'] = reverse('registration:user_register')
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
            user_form = UserForm()
            context['user_form'] = user_form
            context['btn_title'] = 'Авторизация'
            context['url_btn'] = reverse('registration:user_login')
            context['title_page'] = 'Регистрация'
            return render(request, 'registration_app/register.html', context)
    else:
        user_form = UserForm()
        context['user_form'] = user_form
        context['btn_title'] = 'Авторизация'
        context['url_btn'] = reverse('registration:user_login')
        context['title_page'] = 'Регистрация'
        return render(request, 'registration_app/register.html', context)


def user_logout(request):
    logout(request)
    return redirect('registration:user_login')
