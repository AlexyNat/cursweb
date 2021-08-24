from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, SubscriptionForm, TypeSubscriptionForm, ScheduleForm, ReportForm
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .models import Subscription, TypeSubscription, Schedule
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.http import HttpResponse


def index(request):
    return render(request, 'site/index.html', {'title': 'Главная'})


def profile(request):
    if request.user.is_anonymous:
        return redirect('index')

    group = request.user.groups.all().first()
    data = {'title': 'Профиль', 'Роль': group.name}
    if group.name == 'Клиент':
        subscription = Subscription.objects.filter(profile=request.user).first()
        data.update({'Sub': subscription})

    else:
        data.update({'TypeSubs': TypeSubscription.objects.all()})

    return render(request, 'site/profile.html', data)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(Group.objects.get(name='Клиент'))
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/registration.html', {'form': form, 'title': 'Регистрация'})


def createSubscription(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print('error')

    else:
        form = SubscriptionForm(initial={'profile': request.user})

    return render(request, 'site/createabon.html', {'form': form})


def SubscriptionView(request):
    if request.user.is_anonymous:
        return redirect('index')

    group = request.user.groups.all().first()
    data = {'title': 'Абонемент', 'Роль': group.name}
    if group.name == 'Клиент':
        subscription = Subscription.objects.filter(profile=request.user).first()
        data.update({'Sub': subscription})
        return render(request, 'site/subscription.html', data)
    return redirect('home')


def deleteSubscription(request):
    Subscription.objects.filter(profile=request.user).delete()
    return redirect('home')


def pdfView(request):
    response = HttpResponse(content_type='application/pdf')
    subscription = Subscription.objects.filter(profile=request.user).first()

    p = canvas.Canvas(response)
    p.setTitle('Абонемент')
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    p.setFont('Vera', 15)

    p.drawString(15, 660, 'Логин: ' + request.user.username)
    p.drawString(15, 640, 'Пол: ' + request.user.gender)
    p.drawString(15, 620, 'Место жительства: ' + request.user.location)
    p.drawString(15, 600, 'Дата рождения: ' + str(request.user.birth_date))
    p.drawString(15, 580, 'Название абонемента: ' + subscription.type.name)
    p.drawString(15, 560, 'Дата начала использования абонемента: ' + str(subscription.startUse))

    p.showPage()
    p.save()
    return response


# Type Sub
def deleteSubType(request, name):
    if request.user.is_anonymous:
        return redirect('index')

    TypeSubscription.objects.get(name=name).delete()
    return redirect('home')


def createSubType(request):
    if request.method == 'POST':
        form = TypeSubscriptionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print('error')

    else:
        form = TypeSubscriptionForm()

    return render(request, 'site/createabon.html', {'form': form})


def editSubType(request, name):
    if request.user.is_anonymous:
        return redirect('index')

    if request.method == 'POST':
        val = get_object_or_404(TypeSubscription, name=name)
        form = TypeSubscriptionForm(request.POST or None, instance=val)

        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print('error')

    else:
        val = TypeSubscription.objects.get(name=name)
        data = {'name': val.name, 'price': val.price, 'description': val.description, 'duration': val.duration}
        form = TypeSubscriptionForm(initial=data)

    return render(request, 'site/createabon.html', {'form': form})


def ScheduleView(request):
    if request.user.is_anonymous:
        return redirect('index')

    group = request.user.groups.all().first()
    data = {'title': 'Записи', 'Роль': group.name}
    if group.name == 'Клиент':
        subscription = Subscription.objects.filter(profile=request.user).first()

        if subscription is None:
            return redirect('index')

        records = Schedule.objects.filter(subscription=subscription)
        data.update({'Recs': records})
        return render(request, 'site/records/index.html', data)
    return redirect('home')


def ScheduleCreate(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('records')
        else:
            print('error')

    else:
        subscription = Subscription.objects.filter(profile=request.user).first()
        form = ScheduleForm(initial={'subscription': subscription})

    return render(request, 'site/records/create.html', {'form': form})


def ScheduleDelete(request, id):
    if request.user.is_anonymous:
        return redirect('index')

    Schedule.objects.get(id=id).delete()
    return redirect('records')


def reportIndex(request):
    data = {'title': 'Отчет'}

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['dateStart']
            end = form.cleaned_data['dateEnd']

            result = Schedule.objects.filter(recordStartData__range=[start, end]).count()
            data.update({'count': result, 'range': (start, end)})
            return render(request, 'site/ report/index.html', data)

    else:
        form = ReportForm()
    data.update({'form': form})
    return render(request, 'site/ report/index.html', data)
