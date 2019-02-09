from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from .models import config
from .forms import configCreateForm, configModForm
import datetime
import logging
# Create your views here.

def get_all_fields_from_form(instance):
    """"
    Return names of all available fields from given Form instance.

    :arg instance: Form instance
    :returns list of field names
    :rtype: list
    """

    fields = list(instance().base_fields)

    for field in list(instance().declared_fields):
        if field not in fields:
            fields.append(field)
    return fields
def write_to_binary(values):
    logging.debug(values)
    sum = 0
    internal_list = []
    internal_binary_list = []
    internal_template_list = [1,8,8,4,4,
    8,8,8,8,8,
    8,8,16,16,16,
    4,8,16,4,8,
    32,1,32,2,1,
    1,1,1,1,1,
    1,1,1,1,1,
    1,1,1,1,32]
    for i in internal_template_list:
        sum = sum + i
    logging.debug(sum)
    logging.debug(len(internal_template_list))
    for i in values:
        if (isinstance(i, str)):
            if i == "on":
                internal_list.append(1)
            elif i == "off":

                internal_list.append(0)
            else:
                new_f = float(i) #rounding error here
                new_i = int(new_f)

                internal_list.append(new_i)
        else:
            raise Exception("Unknown Type Error")
    logging.debug(internal_list)
    for i in range(0,len(internal_list)):
        internal_binary_list.append(bin(internal_list[i])[2:].zfill(internal_template_list[i]))
    for i in range(len(internal_binary_list)):
        if len(internal_binary_list[i]) == internal_template_list[i]:
            logging.debug('ok')
        else:
            logging.debug("Element {} is wrong. Binary value is {}. template value is {}".format(i, internal_binary_list[i], internal_template_list[i]))
    logging.debug(internal_binary_list)
    internal_binary_string = bin(int(''.join(internal_binary_list),2))[2:]
    logging.debug(internal_binary_string)
    logging.debug(len(internal_binary_string))
    output_file = open('myfile.bin','w')
    output_file.write(internal_binary_string)
    output_file.close()
    return internal_list

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
            configCounter = self.kwargs["pk"]
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
            config.objects.filter(id=newConfigObject.id).update(date_modified=datetime.datetime.now())
            config.objects.filter(id=newConfigObject.id).update(date_submitted=originalDate)
            config.objects.filter(id=newConfigObject.id).update(id=self.kwargs["pk"])

            return HttpResponseRedirect('/configThanks')

        else:
            config.objects.filter(id=self.kwargs["pk"]).delete()
            return HttpResponseRedirect('/delThanks')
class SendDataView(generic.TemplateView):
    model = config
    template_name = 'configUp/sendData.html'
    configLoaded = False

    def get(self, request, *args, **kwargs):
        if not self.configLoaded:
            configCounter = self.kwargs["pk"]
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
            config.objects.filter(id=newConfigObject.id).update(confirmed_uplink=True)


            list_of_fields = get_all_fields_from_form(configModForm)
            newConfigBinary = []
            logging.debug('test')
            for i in range(0, len(list_of_fields)):
                if request.POST.get(list_of_fields[i]) == None:
                    logging.debug(list_of_fields[i])
                    continue
                else:
                    logging.debug("Request Parameter found")
                    newConfigBinary.append(request.POST.get(list_of_fields[i]))

            write_to_binary(newConfigBinary)

            return HttpResponseRedirect('/configThanks')
        else:
            raise Exception("gg")
