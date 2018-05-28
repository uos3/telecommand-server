from django.http import HttpResponse
from django.shortcuts import render
from .forms import EnterCommandForm

def index (request):
    form = EnterCommandForm()
    return render(request, 'command/index.html', { 'form': form })

def send (request):#, command):
    form = EnterCommandForm(request.POST)

    if form.is_valid():
        cmd = form.cleaned_data['command']

        # save command to db, actually send/schedule it etc.
        print('recieved command:', cmd)

        return HttpResponse("Command sent.")
    else:
        return HttpResponse("Bad command!")
