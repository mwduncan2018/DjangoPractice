from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.http.request import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse

from django.core.mail import send_mail
from mduncan2600.settings import EMAIL_HOST_USER

from .forms import NameForm, MessageForm


class Message:
    def __init__(self, id, submitted_by, text, mood, datetime):
        self.id = id
        self.submitted_by = submitted_by
        self.text = text
        self.mood = mood
        self.datetime = datetime
    def __str__(self):
        return str(self.text) + " (" + str(self.submitted_by) + ")"
            
message_list = []
message_list.append(Message(1, 'Mike','Hello Message','CoffeeMood!', 'DateTimeNow'))
message_list.append(Message(2, 'Trav','Hello VideoGame','HaloMood!', 'DateTimeNow'))
message_list.append(Message(3, 'Gail','Hello MysteryShop','MysteryMood!', 'DateTimeNow'))
message_list.append(Message(4, 'Bill','Hello Softball','SoftballMood!', 'DateTimeNow'))


def create(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            submitted_by = form.cleaned_data['submitted_by']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            i_am_gay = form.cleaned_data['i_am_gay']
            
            send_mail(' - '.join(['Post Something', submitted_by]),
                message,
                EMAIL_HOST_USER, [email],
                fail_silently=False,
            )
            
            return HttpResponseRedirect('/messageboard/')
    else:
        message_form = MessageForm()
        context = {
            'message_form': message_form,
        }
        return render(request, 'messageboard/create.html', context)


def index(request):
    context = {
        'album': 'Scenes From A Memory',
        'message_list': message_list,
    }
    return render(request, 'messageboard/index.html', context)
    
    
def edit(request, id):
    print(str(id))
    message = list(filter(lambda x: x.id == id, message_list))[0]
    context = {
        'message': message,
    }
    print(str(message.id))
    print(str(message.text))
    return render(request, 'messageboard/edit.html', context)
    
    
def details(request, id):
    context = {
        'message': 'hey details page',
    }
    return render(request, 'messageboard/details.html', context)
    
    
def delete(request, id):
    context = {
        'message': 'hey delete page',
    }
    return render(request, 'messageboard/delete.html', context)