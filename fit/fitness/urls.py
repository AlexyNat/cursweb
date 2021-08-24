from django.urls import path, include


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='home'),

    path('deleteTypeSub/<str:name>/', views.deleteSubType, name='deletetypesub'),
    path('createTypeSub', views.createSubType, name='createtypesub'),
    path('editTypeSub/<str:name>/', views.editSubType, name='editetypesub'),


    path('records/', views.ScheduleView, name='records'),
    path('createRecord/', views.ScheduleCreate, name='createRecord'),
    path('deleteRecord/<int:id>', views.ScheduleDelete, name='deleteRecord'),

    path('report/index/', views.reportIndex, name='report'),

    path('registration/', views.register, name='signup'),
    path('createabon/', views.createSubscription, name='createabon'),
    path('subscription/', views.SubscriptionView, name='subscription'),
    path('pdfView/', views.pdfView, name='pdfView'),
    path('deleteSubscription/', views.deleteSubscription, name='delete'),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
]
