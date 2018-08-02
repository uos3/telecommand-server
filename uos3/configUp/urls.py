from django.urls import path

from . import views

app_name = 'configUp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('configUp', views.ConfigUpView.as_view(), name='configUpd'),
    path('configThanks', views.ThanksView.as_view(
        template_name="configUp/configThanks.html"), name='configThanks'),
    path('listConfigs', views.ListConfigsView.as_view(), name='listConfigs'),
    path('configDet/<int:pk>', views.ConfigUpView.as_view(
        template_name="configUp/detail.html"), name='detail'),
    path('delThanks', views.ThanksView.as_view(
        template_name="configUp/delThanks.html"), name='delThanks'),
]
