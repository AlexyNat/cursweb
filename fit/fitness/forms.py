from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Subscription, TypeSubscription, Schedule
from django import forms
from django.core.exceptions import ValidationError
import datetime
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ("username", "email", "gender")

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        fields = ('startUse', 'type', 'profile')
        widgets = {'profile': forms.HiddenInput()}


class TypeSubscriptionForm(ModelForm):
    class Meta:
        model = TypeSubscription
        fields = ('name', 'price', 'description', 'duration')


class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ('recordStartData', 'recordStartTime', 'recordTime', 'gym', 'subscription')
        widgets = {'subscription': forms.HiddenInput(),
                   'recordStartData': forms.DateInput(attrs={'type': 'date'}),
                   'recordStartTime': forms.TimeInput(attrs={'type': 'time'}),
                   }


def validateDateStart(date: datetime.date):
    if date < datetime.date(year=2020, month=1, day=1):
        raise ValidationError(
            _('%(value)s дата слишком старая'), params={'value': date},
        )


def validateDateEnd(date: datetime.date):
    if date > datetime.date.today():
        raise ValidationError(
            _('Дата не может быть больше %(value)s (Сегодня)'), params={'value': datetime.date.today()}
        )


class ReportForm(forms.Form):
    validates = [validateDateStart, validateDateEnd]

    dateStart = forms.DateField(label='Дата с',
                                widget=forms.DateInput(attrs={'type': 'date'}),
                                validators=[validates[0]])
    dateEnd = forms.DateField(label='Дата до', widget=forms.DateInput(attrs={'type': 'date'}),
                              validators=[validates[1]])
