from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, TypeSubscription, Subscription, Schedule, Gym


@admin.register(TypeSubscription)
class TypeSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

    @admin.display(description='Премиум')
    def status(self, obj):
        return obj.price > 2000


@admin.register(Subscription)
class TypeSubscription(admin.ModelAdmin):
    list_display = ('startUse', 'GetName')


@admin.register(Schedule)
class TypeSubscription(admin.ModelAdmin):
    list_display = ('Subscription', 'recordStartData', 'recordStartTime', 'End')


@admin.register(Gym)
class TypeSubscription(admin.ModelAdmin):
    list_display = ('name', 'status')


@admin.register(Profile)
class TypeSubscription(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'email', 'groups', 'is_staff', 'is_superuser')
        }),
        ('Последний вход', {
            'fields': ('last_login', )
        }),
        ('Дата регистрации', {
            'fields': ('date_joined', )
        }),
        ('Дополнительно', {
            'fields': ('first_name', 'last_name', 'user_permissions', 'location', 'birth_date', 'gender'),
        }),
    )



