from django.urls import path, include


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='home'),

    path('profile/deleteTypeSub/<str:name>/', views.deleteSubType, name='deletetypesub'),
    path('profile/createTypeSub', views.createSubType, name='createtypesub'),
    path('profile/editTypeSub/<str:name>/', views.editSubType, name='editetypesub'),


    path('profile/records/', views.ScheduleView, name='records'),
    path('profile/records/createRecord/', views.ScheduleCreate, name='createRecord'),
    path('profile/records/deleteRecord/<int:id>', views.ScheduleDelete, name='deleteRecord'),


    # отчет
    path('profile/report/index/', views.reportIndex, name='report'),


    path('profile/createabon/', views.createSubscription, name='createabon'),
    path('profile/subscription/', views.SubscriptionView, name='subscription'),
    path('profile/pdfView/', views.pdfView, name='pdfView'),
    path('profile/deleteSubscription/', views.deleteSubscription, name='delete'),

    # регистрация через свою модель
    path('registration/', views.register, name='signup'),
    # стандарные пресеты
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
]
