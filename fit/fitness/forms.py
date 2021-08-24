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

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        for field in self.fields:

            if field == 'password1':
                self.fields[field].help_text = 'Пароль должен быть больше 8 символов'
            elif field == 'birth_date':
                self.fields[field].help_text = 'Дата рождения не менее ' + str(datetime.date(year=1900, month=1, day=1))
            else:
                self.fields[field].help_text = None

    class Meta:
        model = Profile
        fields = ("username", "email", "gender", 'birth_date', 'location')
        widgets = {'birth_date': forms.DateInput(attrs={'type': 'date'})}

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


def validateDateStartUse(date: datetime.date):
    if date < datetime.date.today():
        raise ValidationError(
            _('%(value)s - дата не может быть раньше сегодня'), params={'value': date},
        )


class SubscriptionForm(ModelForm):
    validate = [validateDateStartUse]

    class Meta:
        model = Subscription
        fields = ('startUse', 'type', 'profile')
        widgets = {'profile': forms.HiddenInput(), 'startUse': forms.DateInput(attrs={'type': 'date'})}

    def clean(self):
        cleaned_data = super(SubscriptionForm, self).clean()
        self.validate[0](cleaned_data.get('startUse'))  # validate


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


class ReportForm(forms.Form):
    validates = [validateDateStart]

    dateStart = forms.DateField(label='Дата с',
                                widget=forms.DateInput(attrs={'type': 'date'}),
                                validators=[validates[0]])
    dateEnd = forms.DateField(label='Дата до', widget=forms.DateInput(attrs={'type': 'date'}), )
