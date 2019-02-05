from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from .models import config
from .forms import configCreateForm, configModForm
# Create your views here.


class IndexView(generic.TemplateView):
    template_name = 'configUp/index.html'


class ThanksView(generic.TemplateView):
    template_name = 'configUp/configThanks.html'


class ConfigUpView(generic.TemplateView):
    template_name = 'configUp/configUp.html'

    def get(self, request, *args, **kwargs):
        if self.template_name == 'configUp/configUp.html':
            form = configCreateForm(initial={
                'power_rail_1': 1,
                'power_rail_3': 1,
                'power_rail_5': 1,
                'power_rail_6': 1,
            })
        else:
            form = configModForm(initial={
            })
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if self.template_name == 'configUp/configUp.html':
            form = configCreateForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('configThanks')


class ListConfigsView(generic.ListView):
    model = config
    template_name = 'configUp/listConfigs.html'

class DetView(generic.TemplateView):
     model = config
     template_name = 'configUp/detail.html'
     configLoaded = False

     def get(self, request, *args, **kwargs):
         if not self.configLoaded:
             configCounter = self.kwargs["pk"]
             configObject = config.objects.filter(id=self.kwargs["pk"])
             valuesDict = configObject.values()[0]
             form = configModForm(initial=valuesDict)
             self.configLoaded = True
             return render(request, self.template_name, {'form': form, 'configCounter': configCounter})


class ModDetView(generic.TemplateView):
    model = config
    template_name ='configUp/modDetail.html'
    configLoaded = False

    def get(self, request, *args, **kwargs):
        if not self.configLoaded:
            configObject = config.objects.filter(id=self.kwargs["pk"])
            valuesDict = configObject.values()[0]
            form = configModForm(initial=valuesDict)
            self.configLoaded = True
            return render(request, self.template_name, {'form': form, 'configCounter': configCounter})

    def post(self, request, *args, **kwargs):
        form = configModForm(request.POST)
        if form.is_valid():
            form.save()
            newConfigObject = config.objects.latest('date_submitted')
            configObject = config.objects.filter(id=self.kwargs["pk"])
            originalDate = configObject[0].date_submitted

            config.objects.filter(id=self.kwargs["pk"]).delete()
            config.objects.filter(id=newConfigObject.id).update(date_submitted=originalDate)
            config.objects.filter(id=newConfigObject.id).update(id=self.kwargs["pk"])
            return HttpResponseRedirect('/configThanks')

        else:
            config.objects.filter(id=self.kwargs["pk"]).delete()
            return HttpResponseRedirect('delThanks')
class SendDataView(generic.TemplateView):
    model = config
    template_name = 'configUp/sendData.html'
    configLoaded = False

    def get(self, request, *args, **kwargs):
        if not self.configLoaded:
            configObject = config.objects.filter(id=self.kwargs["pk"])
            valuesDict = configObject.values()[0]
            form = configModForm(initial=valuesDict)
            self.configLoaded = True
            return render(request, self.template_name, {'form': form, 'configCounter': configCounter})
