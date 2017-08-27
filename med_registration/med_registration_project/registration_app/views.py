from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from .forms import UserForm
from .models import Doctors, Specialty, Schedule

from calendar import Calendar
from datetime import time, datetime as dt


def get_datetime(args):

    # Блок получающий актуальные даты текущего месяца
    dates = Calendar(0).itermonthdates(dt.today().year, dt.today().month)
    NOW = dt.today().date()
    actual_dates = [date for date in dates if date >= NOW]

    WORK_DATES = []
    WORK_TIME = [time(t, 00) for t in range(9, 19)]
    for ac_date in actual_dates:
        for work_hour in WORK_TIME:
            WORK_DATES.append(dt.combine(ac_date, work_hour))

    # Извлекаем из queryset данные. Не понимаю почему, но через for не хочет работать, требует целочисленный индекс у args
    i = 0
    qs_dates = []
    while i < len(args):
        qs_dates.append(dt.combine(dt.date(args[i]['pub_date']), dt.time(args[i]['pub_date'])))
        i += 1

    # Получаем список свободных дней и часов для записи к врачу
    [WORK_DATES.remove(work_date) for work_date in WORK_DATES if work_date in qs_dates]

    # Сериализуем данные в два списка: 1) отсортированный список дат; 2) отсортированный список времени
    # Сортируем список по времени
    work_days = sorted(set([dt.date(work_date) for work_date in WORK_DATES]))

    # Создаем словарь дата: [время]
    DATES_DICT = {}
    buff_lst = []
    for work_day in work_days:
        for work_date in WORK_DATES:
            if work_day == dt.date(work_date):
                buff_lst.append(dt.time(work_date).hour)
        DATES_DICT[work_day] = buff_lst
        buff_lst = []

    # Разбиваем словарь на два списка и возвращаем все в datetime_list + словарь дата: время
    date_list = sorted(list(DATES_DICT.keys()))
    time_list = []
    for i in date_list:
        time_list.append(DATES_DICT[i])
    return [date_list, time_list, DATES_DICT]


def schedule(request, id=None):
    if request.user.is_authenticated():
        current_date = dt.combine(dt.today().date(), time(0, 0))
        schedule_query = Schedule.objects.filter(doctor__id=id, pub_date__gte=current_date).order_by('pub_date').values()
        datetime_list = get_datetime(schedule_query)
        context = {
            'work_dates': datetime_list[0],
            'work_times': datetime_list[1],
            'dates_dict': datetime_list[2],
            'doctor': get_object_or_404(Doctors, id=id),
            'btn_state': 'Выйти',
            'url_state': reverse('registration:user_logout'),
            'title_page': 'Расписание приема посетителей',
        }
        return render(request, 'registration_app/schedule.html', context)
    else:
        return redirect('registration:user_login')


def record_list(request, id, year, month, day, hour):
    if request.user.is_authenticated():
        str_date = '{}/{}/{} {}:00'.format(year, month, day, hour)
        format_str = "%Y/%m/%d %H:%M"
        context = {
            'client': '{} {}'.format(request.user.first_name, request.user.last_name),
            'doctor': get_object_or_404(Doctors, id=id),
            'record_date': dt.strptime(str_date, format_str).date(),
            'record_time': dt.strptime(str_date, format_str).time(),
            'btn_state': 'Выйти',
            'url_state': reverse('registration:user_logout'),
            'title_page': 'Лист записи',
        }
        record = Schedule(client=context['client'],
                          pub_date=dt.combine(context['record_date'], context['record_time']),
                          doctor=context['doctor'],
                          specialty=context['doctor'].specialty
                          )
        record.save()
        return render(request, 'registration_app/record_list.html', context)
    else:
        return redirect('registration:user_login')


def doctors_list(request):
    if request.user.is_authenticated():
        context = {
            'doctors': Doctors.objects.all().order_by('specialty'),
            'specialty': Specialty.objects.all().order_by('id'),
            'btn_state': 'Выйти',
            'url_state': reverse('registration:user_logout'),
            'title_page': 'Специалисты клиники',
        }
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
            user_form = UserForm()
            context['user_form'] = user_form
            context['btn_state'] = 'Регистрация'
            context['url_state'] = reverse('registration:user_register')
            context['title_page'] = 'Авторизация'
            return render(request, 'registration_app/login.html', context)
    else:
        user_form = UserForm()
        context['user_form'] = user_form
        context['btn_state'] = 'Регистрация'
        context['url_state'] = reverse('registration:user_register')
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
            context['btn_state'] = 'Авторизация'
            context['url_state'] = reverse('registration:user_login')
            context['title_page'] = 'Регистрация'
            return render(request, 'registration_app/register.html', context)
    else:
        user_form = UserForm()
        context['user_form'] = user_form
        context['btn_state'] = 'Авторизация'
        context['url_state'] = reverse('registration:user_login')
        context['title_page'] = 'Регистрация'
        return render(request, 'registration_app/register.html', context)


def user_logout(request):
    logout(request)
    return redirect('registration:user_login')
