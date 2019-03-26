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
    logging.debug(len(values))
    sum = 0
    internal_list = []
    internal_template_list = [1,8,8,4,4, #41 parameters
    8,8,8,8,8,
    8,8,16,16,16,
    4,8,16,4,8,
    32,1,32,2,1,
    1,1,1,1,1,1,
    1,1,1,1,1,
    1,1,1,1,32] #power_rail_4 is missing from configuration file spreadsheet

    internal_bytes = bytearray()
    for i in internal_template_list:
        sum = sum + i

    logging.debug(sum)
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
    for counter in range(0, len(internal_list)):
        if internal_list[counter] < 255:
            internal_bytes.append(internal_list[counter])
        elif internal_list[counter] > 255:
            bit_counter = int(internal_template_list[counter]/8)
            logging.debug("Larger than 255 value encountered. Value is {}, attempting to convert to bytes. Template bits length is {}".format(internal_list[counter], internal_template_list[counter]))
            #result = internal_list[counter].to_bytes(bit_counter, 'little')
            #internal_bytes[counter:counter] = result
            #logging.debug("Output is {}".format(result))
            #logging.debug("Testing reverse: {}".format(int.from_bytes(result, 'little')))
            for i in range(1, bit_counter + 1):
                bitshift = 32-(8*i)
                result = internal_list[counter] << (bitshift) & 0xFF
                internal_bytes.append(result)
                logging.debug("Bitshifting value of {} by {}, result is {}".format(internal_list[counter], bitshift, result))
    logging.debug(internal_bytes)
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
                'power_rail_2': 1,
                'power_rail_3': 1,
                'power_rail_4': 1,
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
            else:
                raise Exception(form.errors.as_text())

class ListConfigsView(generic.ListView):
    model = config
    template_name = 'configUp/listConfigs.html'

class ListConfigsSentView(generic.ListView):
    model = config
    template_name = 'configUp/listConfigsSent.html'

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
        logging.debug("Config Object ID: {} has been found".format(self.kwargs["pk"]))

        if form.is_valid():
            form.save()

            list_of_fields = get_all_fields_from_form(configModForm)
            newConfigBinary = []

            for i in range(0, len(list_of_fields)):
                if request.POST.get(list_of_fields[i]) == None:
                    logging.debug(list_of_fields[i])
                    continue
                else:
                    newConfigBinary.append(request.POST.get(list_of_fields[i]))

            write_to_binary(newConfigBinary)

            config.objects.filter(id=self.kwargs["pk"]).update(confirmed_uplink = True)
            
            logging.debug("Config Object ID: {} has been updated".format(self.kwargs["pk"]))


            return HttpResponseRedirect('/configThanks')
        else:
            raise Exception("gg")
