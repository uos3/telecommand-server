from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import config
from .forms import ConfigForm
# Create your views here.


class IndexView(generic.TemplateView):
    template_name = 'configUp/index.html'


class ConfigView(generic.DetailView):
    model = config
    template_name = 'configUp/config.html'
