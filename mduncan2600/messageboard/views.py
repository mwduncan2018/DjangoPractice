import random
import datetime

#from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
class DecimalEncoder(json.JSONEncoder):
    def default(self, x):
        if isinstance(x, decimal.Decimal):
            if x % 1 > 0:
                return float(x)
            else:
                return int(x)
        return super(DecimalEncoder, self).default(x)

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.http.request import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse

from django.core.mail import send_mail
from mduncan2600.settings import EMAIL_HOST_USER

from .forms import NameForm, MessageForm


class Message:
    def __init__(self, submitted_by, message, mood, datetime):
        self.id = id
        self.submitted_by = submitted_by
        self.message = message
        self.mood = mood
        self.datetime = datetime
    def __str__(self):
        return str(self.message) + " (" + str(self.submitted_by) + ")"
            
message_list = []
message_list.append(Message('Rabbit', 'OMG I\'m tripping BALLSSS', 'TRIPPIN BALLS', str(datetime.datetime.now())))
message_list.append(Message('Rabbit', 'Ur so gay, Lion', 'TRIPPING BALLS', str(datetime.datetime.now())))
message_list.append(Message('Lion', '>:O', 'ANGRY', str(datetime.datetime.now())))
message_list.append(Message('Grizzly', 'Dude, Lion just ate Rabbit', 'DRUNK', str(datetime.datetime.now())))
message_list.append(Message('Owl', 'It is a beautiful day for perching', 'HAPPY', str(datetime.datetime.now())))
message_list.append(Message('Grizzly', 'Shut up you fag owl I\'m tired of ur shit', 'DRUNK', str(datetime.datetime.now())))


def how_to_send_email(submitted_by, message):
    send_email = True
    if send_email:
        send_mail(' - '.join(['Post Something', str(random.Random().randint(1, 1000000))]),
            ': '.join([submitted_by, message]),
            EMAIL_HOST_USER,
            ['mduncan2600@gmail.com'],
            fail_silently=False,
        )


def splash(request):
    return HttpResponse("Du!")


def animal_conversation(request):
    response = (boto3
        .resource('dynamodb', region_name='us-east-1')
        .Table('PostSomethingAnimalConversations')
        .scan())
    message_list = []
    for j in response['Items']:
        message = Message(j['SubmittedBy'], j['Message'], j['Mood'], j['DateTime'])
        message_list.append(message)
    context = {
        'message_list': message_list,
    }
    return render(request, 'messageboard/animal-conversation.html', context)


def add_post(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            submitted_by = form.cleaned_data['submitted_by']
            message = form.cleaned_data['message']
            mood = form.cleaned_data['mood']
            now = datetime.datetime.now()
            
            #######################
            # Continue here tomorrow
            # Finish adding to DynamoDB
            #
            # Then do the Bootstrap 4 Chat
            #######################
            
            
            return HttpResponseRedirect('/messageboard/')
    else:
        message_form = MessageForm()
        context = {
            'message_form': message_form,
        }
        return render(request, 'messageboard/add-post.html', context)


def clear_conversation(request):
    print(str(id))
    message = list(filter(lambda x: x.id == id, message_list))[0]
    context = {
        'message': message,
    }
    print(str(message.id))
    print(str(message.text))
    return render(request, 'messageboard/clear-conversation.html', context)
    

# DELETE THIS LATER    
def view_animals(request):
    context = {
        'message': 'hey details page',
    }
    return render(request, 'messageboard/viewanimals.html', context)
    
    
def about(request):
    context = {
        'message': 'hey delete page',
    }
    return render(request, 'messageboard/about.html', context)