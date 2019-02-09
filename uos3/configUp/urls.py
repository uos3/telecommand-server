from django.urls import path

from . import views

app_name = 'configUp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('configUp', views.ConfigUpView.as_view(template_name = "configUp/configUp.html"), name='configUpd'),
    path('configThanks', views.ThanksView.as_view(
        template_name="configUp/configThanks.html"), name='configThanks'),
    path('listConfigs', views.ListConfigsView.as_view(), name='listConfigs'),
    path('configDet/<int:pk>', views.DetView.as_view(
        template_name="configUp/detail.html"), name='detail'),
    path('delThanks', views.ThanksView.as_view(
        template_name="configUp/delThanks.html"), name='delThanks'),
    path('configDet/configThanks', views.ThanksView.as_view(
        template_name="configUp/configThanks.html"), name='configThanks'),
    path('configModDet/<int:pk>', views.ModDetView.as_view(
        template_name="configUp/modDetail.html"), name='modDetail'),
    path('configSend/<int:pk>', views.SendDataView.as_view(
        template_name="configUp/sendData.html"), name='sendData'),
]
