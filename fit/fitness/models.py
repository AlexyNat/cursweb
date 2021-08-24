from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib import admin
from dateutil.relativedelta import relativedelta
from django.utils import timezone


class Profile(AbstractUser):
    genders = (('М', 'Мужчина'), ('Ж', 'Женщина'))
    location = models.CharField(max_length=150, blank=True, verbose_name='Адрес')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    gender = models.CharField('Пол', choices=genders, max_length=1, default='М')

    def __str__(self):
        return self.username


class TypeSubscription(models.Model):
    choices = (('Год', 'Год'), ('Пол', 'Полгода'), ('Мес', 'Месяц'), ('Ден', 'День'))
    name = models.CharField('Название абонемента', primary_key=True, max_length=50)
    price = models.FloatField('Цена')
    description = models.TextField('Описание')
    duration = models.CharField('Время действия', max_length=3, choices=choices, default='Год')

    def shortTime(self):
        return self.duration == 'Ден'

    class Meta:
        verbose_name = 'Вид абонемента'
        verbose_name_plural = 'Виды абонементов'
        ordering = ['name']

    def __str__(self):
        return self.name


class Subscription(models.Model):
    startUse = models.DateField(blank=True, verbose_name='Начало пользования')
    type = models.ForeignKey(TypeSubscription, models.CASCADE, verbose_name='Тип абонемента')
    profile = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)

    @admin.display(description='Тип абонемента')
    def GetName(self):
        return self.type.name

    @admin.display(description='Срок действия')
    def GetEnd(self):
        if self.type.duration == 'Год':
            return self.startUse + relativedelta(year=self.startUse.year + 1)
        elif self.type.duration == 'Пол':
            return self.startUse + relativedelta(month=self.startUse.mounth + 6)
        elif self.type.duration == 'Мес':
            return self.startUse + relativedelta(month=self.startUse.mounth + 1)
        else:
            return self.startUse + relativedelta(day=self.startUse.day + 1)

    class Meta:
        verbose_name = 'Абонемент'
        verbose_name_plural = 'Абонементы'
        ordering = ['type']

    def __str__(self):
        return 'Абонемент №' + str(self.id)


class Schedule(models.Model):
    choices = (('Ч', 'Час'), ('П', 'Пол часа'), ('Д', 'Два часа'))
    recordStartData = models.DateField('Дата занятия')
    recordStartTime = models.TimeField('Время занятия')
    recordTime = models.CharField('Продолжительность', choices=choices, max_length=1, default=choices[0])
    gym = models.ForeignKey('Gym', models.CASCADE, verbose_name='Зал')
    subscription = models.ForeignKey(Subscription, models.CASCADE, verbose_name='Абонемент')

    def End(self):
        if self.recordTime == 'Ч':
            return timezone.datetime.combine(self.recordStartData, self.recordStartTime) + timezone.timedelta(hours=1)
        elif self.recordTime == 'П':
            return \
                timezone.datetime.combine(self.recordStartData, self.recordStartTime) + timezone.timedelta(minutes=30)
        else:
            return timezone.datetime.combine(self.recordStartData, self.recordStartTime) + timezone.timedelta(hours=2)

    @admin.display(description='Абонемент')
    def Subscription(self):
        return self.subscription.id

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Расписание'
        ordering = ['recordStartData']

    def __str__(self):
        return 'Запись №' + str(self.id)


class Gym(models.Model):
    name = models.CharField('Название', primary_key=True, max_length=50)
    status = models.BooleanField('Доступность')

    class Meta:
        verbose_name = 'Зал'
        verbose_name_plural = 'Помещения'
        ordering = ['name']

    def __str__(self):
        return self.name
