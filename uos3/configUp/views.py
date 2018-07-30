from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import config
from .forms import configForm
# Create your views here.


class IndexView(generic.TemplateView):
    template_name = 'configUp/index.html'


class ThanksView(generic.TemplateView, type=0):
    if type == 0:
        template_name = 'configUp/configThanks.html'
    else if type == 1:
        template_name = 'configUp/delThanks.html'


class ConfigView(generic.edit.FormView):
    form_class = configForm
    template_name = 'configUp/config.html'
    success_url = '/configThanks/'

    def get_config(request):
        if request.method == 'POST':
            form = configForm(request.POST)
            if form.is_valid():
                return HttpResponseRedirect('/configThanks')
        else:
            form = configForm()
        return render(request, 'config.html', {'form': form})


class ListConfigsView(generic.ListView):
    template_name = 'configUp/listConfigs.html'


class DelView(generic.DetailView):
    template_name = 'configUp/del.html'
