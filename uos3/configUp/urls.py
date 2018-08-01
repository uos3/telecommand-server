from django.urls import path

from . import views

app_name = 'configUp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('configUp.html', views.ConfigUpView.as_view(), name='configUpd'),
    path('configThanks.html', views.ThanksView.as_view(template_name="configUp/configThanks.html"), name='configThanks'),
    path('listConfigs.html', views.ListConfigsView.as_view(), name='listConfigs'),
    path('configDet.html/<int:pk>', views.DetView.as_view(), name='detail'),
    path('delThanks.html', views.ThanksView.as_view(template_name="configUp/delThanks.html"), name='delThanks'),
]
