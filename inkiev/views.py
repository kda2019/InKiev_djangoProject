from django.shortcuts import render, HttpResponseRedirect, Http404, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import auth
from django.template.loader import render_to_string
import datetime
from .models import Event, PrivateEvent, Place, Comment
from .forms import LoginForm, UserRegistrationForm, PrivateEventForm, EventForm, PlaceForm


def f_page(request):
    """Стартовая страница, отображает все сегодняшние события и случайную локацию"""

    pu_events = Event.objects.filter(start_time__date=datetime.date.today(), is_active=True, is_verified=True)
    pr_events = PrivateEvent.objects.filter(start_time__date=datetime.date.today(), is_active=True)
    random_place = Place.objects.filter(is_active=True, is_verified=True).order_by('?').first()
    a = {'pu_events': pu_events, 'pr_events': pr_events, 'place': random_place}
    return render(request, 'today.html', a)


def public_events(request):
    """Страница c актуальными публичными ивентами"""

    events = Event.objects.filter(start_time__date__gte=datetime.date.today(), is_active=True,
                                  is_verified=True).order_by('start_time')
    a = {'events': events, 'h1': 'Список ближайших публичных событий:', 'time_href': '/Event-old/', 'old': False}
    return render(request, 'events.html', a)


def public_events_old(request):
    """Страница c публичными ивентами даты которых уже истекли
    Использует тот же шаблон, что и функция public_events
    """
    events = Event.objects.filter(start_time__date__lt=datetime.date.today(), is_active=True,
                                  is_verified=True).order_by('-start_time')
    a = {'events': events, 'h1': 'Список прошедших публичных событий:', 'time_href': '/Event/', 'old': True}
    return render(request, 'events.html', a)


def private_events(request):
    """Страница с актуальными частными ивентами
    Использует тот же шаблон, что и функция public_events
    """
    events = PrivateEvent.objects.filter(start_time__date__gte=datetime.date.today(), is_active=True).order_by(
        'start_time')
    a = {'events': events, 'h1': 'Список ближайших приватных событий:', 'time_href': '/PrivateEvent-old/', 'old': False}
    return render(request, 'events.html', a)


def private_events_old(request):
    """Страница с частными ивентами даты которых уже истекли
    Использует тот же шаблон, что и функция public_events
    """
    events = PrivateEvent.objects.filter(start_time__date__lt=datetime.date.today(), is_active=True).order_by(
        '-start_time')
    a = {'events': events, 'h1': 'Список прошедших приватных событий:', 'time_href': '/PrivateEvent/', 'old': True}
    return render(request, 'events.html', a)


def places(request):
    """Список всех локаций"""

    _places = Place.objects.filter(is_active=True, is_verified=True)
    a = {'places': _places}
    return render(request, 'places.html', a)


def place_page(request, p_pk):
    """Страница локации.
    Принимает id локации
    Возыращает страницу с описанием локации или 404
    """
    place = get_object_or_404(Place, pk=p_pk)
    if (place.is_verified and place.is_active) or request.user.is_staff:
        a = {'place': place}
        return render(request, 'place.html', a)
    else:
        raise Http404


def public_event_page(request, e_pk):
    """Страница публичного ивента.
    Принимает id публичного ивента
    Возыращает страницу с описанием ивента, коментариями и формой к ним или 404
    Так же обрабатывает POST запрос на добавление нового коментария
    """
    event = get_object_or_404(Event, pk=e_pk)
    if (event.is_verified and event.is_active) or request.user.is_staff:
        if request.method == 'GET':
            comments = event.comments.all()
            a = {'event': event, 'comments': comments}
            return render(request, 'event.html', a)
        elif request.method == 'POST':
            if request.user.is_authenticated:
                comment = request.POST.get('comment')
                Comment.objects.create(text=comment, content_object=event, user=request.user)
                return HttpResponseRedirect(request.get_full_path())
            else:
                HttpResponseRedirect('/')
    else:
        raise Http404


def private_event_page(request, e_pk):
    """Страница приватного ивента.
    Принимает id приватного ивента
    Возыращает страницу с описанием ивента, коментариями и формой к ним или 404
    Так же обрабатывает POST запрос на добавление нового коментария
    """
    event = PrivateEvent.objects.get(pk=e_pk)
    if event.is_active or request.user.is_staff:
        if request.method == 'GET':
            comments = event.comments.all()
            a = {'event': event, 'comments': comments}
            return render(request, 'event.html', a)
        elif request.method == 'POST':
            if request.user.is_authenticated:
                comment = request.POST.get('comment')
                Comment.objects.create(text=comment, content_object=event, user=request.user)
                return HttpResponseRedirect(request.get_full_path())
    else:
        raise Http404


def comment_remove(request, c_pk):
    """Пользователь может удалить комментарий в 2 случаях:
    1)Если пользователь имеет права админа.
    2)Если коментарий принадлежит пользователю.
    -------
    Принимает на вход:
    1)Имя связанного с комментарием класса поста
    2)id комментария
    -------
    Возвращает обратно на страницу поста или 404
    """
    comment = get_object_or_404(Comment, pk=c_pk)
    if comment.user == request.user or request.user.is_staff:
        comment.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        raise Http404


def user_login(request):
    """Работает с ajax запросами
    При первом запросе возвращает форму
    При отправке формы проводит пытается авторизировать и возвращает результат
    """
    if request.user.is_authenticated:
        raise Http404()
    if request.method == "POST":
        if request.POST.get('task') == 'get_form':  # Отправляем формму
            form = LoginForm()
            return JsonResponse({'html': render_to_string('ajax_templates/login.html', {'form': form}, request)})
        else:  # Обрабатываем форму
            log = request.POST.get('login')
            pas = request.POST.get('password')
            user = auth.authenticate(username=log, password=pas)
            if user is not None:
                auth.login(request, user)
                return JsonResponse({'auth': 'ok'})
            else:
                return JsonResponse({'auth': 'bad_auth'})
    else:
        raise Http404()


def logout(request):
    """Выход из учетной записи и переадресация на корневую страницу"""

    auth.logout(request)
    return HttpResponseRedirect('/')


def user_register(request):
    """Работает с ajax запросами
    При первом запросе возвращает форму
    При отправке формы проводит валидацию, после чего
    в случае успеха - регистрирует пользователя и отправляет соответствующее json сообщение
    в случае неудачи - отправляет json сообщение о неудачи со всеми допущенными ошибками
    """
    if request.user.is_authenticated:
        raise Http404()
    if request.method == "POST":
        if request.POST.get('task') == 'get_form':  # Отправляем формму
            form = UserRegistrationForm()
            return JsonResponse({'html': render_to_string('ajax_templates/register.html', {'form': form}, request)})
        else:
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password2'])
                new_user.save()
                return JsonResponse({'valid': True})
            else:
                response = user_form.errors.get_json_data()
                response['valid'] = False
                return JsonResponse(response)


def create_private_event(request):
    """Страница с формой создания частных ивентов.
    При GET запросе - отдает форму
    При POST запросе - сохраняет и перенаправляет на страницу с приватными ивентами,
    либо в случае неудачи сообщает об ошибке.
    """
    if request.user.is_authenticated:
        form = PrivateEventForm()
        if request.method == "GET":
            return render(request, "pages_for_create/create-private-event.html", {'form': form})
        elif request.method == "POST":
            event = PrivateEventForm(request.POST)
            if event.is_valid():
                event = event.save(commit=False)
                event.user = request.user
                event.save()
                return HttpResponseRedirect('/PrivateEvent')
            else:
                form = event
                message = 'Форма не валидна. Возможно указано неверное время'
                return render(request, "pages_for_create/create-private-event.html", {'form': form, 'message': message})


def create_public_event(request):
    """Страница с формой создания публичных ивентов.
    При GET запросе - отдает форму
    При POST запросе - сохраняет и перенаправляет на страницу с публичными ивентами,
    либо в случае неудачи сообщает об ошибке.
    -------------
    В отличии от create_private_event, объекты созданные не модераторами получают флаг is_verified=False
    """
    if request.user.is_authenticated:
        form = EventForm()
        if request.method == "GET":
            return render(request, "pages_for_create/create-public-event.html", {'form': form})
        elif request.method == "POST":
            event = EventForm(request.POST)
            if event.is_valid():
                event = event.save(commit=False)
                if request.user.is_staff:
                    message = 'Событие создано'
                else:
                    event.is_verified = False
                    message = 'Событие отправлено на проверку!'
                event.user = request.user
                event.save()
                return HttpResponseRedirect('/Event')
            else:
                form = event
                message = 'Форма не валидна. Возможно указано неверное время'
                return render(request, "pages_for_create/create-public-event.html", {'form': form, 'message': message})


def create_place(request):
    """Страница с формой добавления локации.
    При GET запросе - отдает форму
    При POST запросе - сохраняет и перенаправляет на страницу с локациями,
    либо в случае неудачи сообщает об ошибке.
    -------------
    Объекты созданные не модераторами получают флаг is_verified=False
    """
    if request.user.is_authenticated:
        form = PlaceForm()
        if request.method == "GET":
            return render(request, "pages_for_create/create-place.html", {'form': form})
        elif request.method == "POST":
            place = PlaceForm(request.POST)
            if place.is_valid():
                place = place.save(commit=False)
                if request.user.is_staff:
                    message = 'Локация добавлена'
                else:
                    place.is_verified = False
                    message = 'Локация отправлена на проверку!'
                place.save()
                return HttpResponseRedirect('/Place')
            else:
                form = place
                message = 'Форма не валидна. Исправьте и попробуйте еще раз'
                return render(request, "pages_for_create/create-place.html", {'form': form, 'message': message})


def unverified_public_events(request, act=None, e_pk=None):
    """Страница на которой отображаются предложенные пользоваетелями публичные ивенты,
    которые можно либо одобрить, либо удалить
    ---------
    Принимает на вход:
    1)Действие ['add'-одобрить, 'del' - удалить]
    2)id ивента
    ---------
    1)При запросе без параметров -  возвращает страницу со списком неподтвержденных ивентов
    2)При запросе с параметрами - Выполняет действие и переадресовыввет на эту же страницу, но без параметров.
    В случае некорректных параметров возвращает 404
    """
    if request.user.is_staff:
        if act is None or e_pk is None:
            events = Event.objects.filter(is_verified=False)
            return render(request, 'pages_for_create/unverified-public-events.html', {'events': events})
        else:
            event = Event.objects.get(pk=e_pk)
            if act == 'add':
                event.is_verified = True
                event.save()
            elif act == 'del':
                event.delete()
            else:
                raise Http404
            return HttpResponseRedirect('/unverified-public-events/')

    else:
        raise Http404


def unverified_places(request, act=None, p_pk=None):
    """Страница на которой отображаются предложенные пользоваетелями локации,
    которые можно либо одобрить, либо удалить
    ---------
    Принимает на вход:
    1)Действие ['add'-одобрить, 'del' - удалить]
    2)id локации
    ---------
    1)При запросе без параметров -  возвращает страницу со списком неподтвержденных локаций
    2)При запросе с параметрами - Выполняет действие и переадресовыввет на эту же страницу, но без параметров.
    В случае некорректных параметров возвращает 404
    """
    if request.user.is_staff:
        if act is None or p_pk is None:
            places_ = Place.objects.filter(is_verified=False)
            return render(request, 'pages_for_create/unverified-places.html', {'places': places_})
        else:
            place_ = Place.objects.get(pk=p_pk)
            if act == 'add':
                place_.is_verified = True
                place_.save()
            elif act == 'del':
                place_.delete()
            else:
                raise Http404
            return HttpResponseRedirect('/unverified-places/')

    else:
        raise Http404


def remove_post(request, post_class, p_pk):
    """Удаляет пост, делая его неактивным
    -------------
    Принимает параметы:
    1)Название класса поста
    2)id поста
    -------------
    Переадресовывает пользователя на страницу с постами того же типа, который имел удаленный
    или возвращает 404
    """
    if request.user.is_staff:
        if post_class == 'Event':
            post = get_object_or_404(Event, pk=p_pk)
        elif post_class == 'PrivateEvent':
            post = get_object_or_404(PrivateEvent, pk=p_pk)
        elif post_class == 'Place':
            post = get_object_or_404(Place, pk=p_pk)
        else:
            raise Http404
        post.is_active = False
        post.save()
        return HttpResponseRedirect('/' + post_class)
    else:
        raise Http404


def deleted_places(request, act=None, p_pk=None):
    """Страница с удаленными модератором локациями, с которой их можно востанавливать
    или безвозвратно удалять
    ---------
    Принимает на вход:
    1)Действие ['undelete'-восстановить, 'remove' - удалить]
    2)id локации
    ---------
    1)При запросе без параметров -  возвращает страницу со списком удаленных локаций
    2)При запросе с параметрами - Выполняет действие и переадресовыввет на эту же страницу, но без параметров.
    В случае некорректных параметров возвращает 404
    """
    if request.user.is_staff:
        if act is None or p_pk is None:
            places_ = Place.objects.filter(is_active=False)
            return render(request, 'pages_for_create/deleted-places.html', {'places': places_})
        else:
            place_ = get_object_or_404(Place, pk=p_pk)
            if act == 'undelete':
                place_.is_active = True
                place_.save()
            elif act == 'remove':
                place_.delete()
            else:
                raise Http404
            return HttpResponseRedirect('/deleted-places/')


def deleted_public_events(request, act=None, e_pk=None):
    """Страница с удаленными модератором публичными ивентами, с которой можно востановить
     или безвозвратно удалить ивент
     ---------
     Принимает на вход:
     1)Действие ['undelete'-восстановить, 'remove' - удалить]
     2)id ивента
     ---------
     1)При запросе без параметров -  возвращает страницу со списком удаленных ивентов
     2)При запросе с параметрами - Выполняет действие и переадресовыввет на эту же страницу, но без параметров.
     В случае некорректных параметров возвращает 404
     """
    if request.user.is_staff:
        if act is None or e_pk is None:
            events = Event.objects.filter(is_active=False)
            return render(request, 'pages_for_create/deleted-public-events.html', {'events': events})
        else:
            event = get_object_or_404(Event, pk=e_pk)
            if act == 'undelete':
                event.is_active = True
                event.save()
            elif act == 'remove':
                event.delete()
            else:
                raise Http404
            return HttpResponseRedirect('/deleted-public-events/')


def deleted_private_events(request, act=None, e_pk=None):
    """Страница с удаленными модератором частными ивентами, с которой можно востановить
     или безвозвратно удалить ивент
     ---------
     Принимает на вход:
     1)Действие ['undelete'-восстановить, 'remove' - удалить]
     2)id ивента
     ---------
     1)При запросе без параметров -  возвращает страницу со списком удаленных ивентов
     2)При запросе с параметрами - Выполняет действие и переадресовыввет на эту же страницу, но без параметров.
     В случае некорректных параметров возвращает 404
     """
    if request.user.is_staff:
        if act is None or e_pk is None:
            events = PrivateEvent.objects.filter(is_active=False)
            return render(request, 'pages_for_create/deleted-private-events.html', {'events': events})
        else:
            event = get_object_or_404(PrivateEvent, pk=e_pk)
            if act == 'undelete':
                event.is_active = True
                event.save()
            elif act == 'remove':
                event.delete()
            else:
                raise Http404
            return HttpResponseRedirect('/deleted-private-events/')
