import random
import datetime
import json
import decimal
import boto3
from boto3.dynamodb.conditions import Key, Attr

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.http.request import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse

from .forms import NameForm, MessageForm


class DecimalEncoder(json.JSONEncoder):
    """Utility class to make JSON pretty when using AWS"""
    def default(self, x):
        if isinstance(x, decimal.Decimal):
            if x % 1 > 0:
                return float(x)
            else:
                return int(x)
        return super(DecimalEncoder, self).default(x)


class MessageViewModel:
    """View Model object to pass to the templates"""
    def __init__(self, submitted_by=None, message=None, mood=None, datetime=None, picture=None):
        self.id = id
        self.submitted_by = submitted_by
        self.message = message
        self.mood = mood
        self.datetime = datetime
        self.picture = picture
    def __str__(self):
        return str(self.message) + " (" + str(self.submitted_by) + ")"


def how_to_send_email(submitted_by, message):
    """Demo of how to send email"""
    from django.core.mail import send_mail
    from mduncan2600.settings import EMAIL_HOST_USER
    send_email = False
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
    
    # Get the data from AWS DynamoDB
    response = (boto3
        .resource('dynamodb', region_name='us-east-1')
        .Table('PostSomethingAnimalConversations')
        .scan())
        
    # Put the data in a List of MessageViewModel
    message_list = []
    for j in response['Items']:
        x_date = datetime.datetime.strptime(j['DateTime'], '%Y-%m-%d %H:%M:%S.%f')

        image_thumbnail_dir = '/static/messageboard/images/thumbnails/'
        thumbnail_dict = {
            'Bison': image_thumbnail_dir + 'Bison_ps.jpg',
            'Black Puma': image_thumbnail_dir + 'BlackPuma_ps.jpg',
            'Elk': image_thumbnail_dir + 'Elk_ps.jpg',
            'Fox': image_thumbnail_dir + 'Fox_ps.jpg',
            'Gorilla': image_thumbnail_dir + 'Gorilla_ps.jpg',
            'Grizzly': image_thumbnail_dir + 'Grizzly_ps.jpg',
            'Hair Bear': image_thumbnail_dir + 'HairBear_ps.jpg',
            'Kangaroo': image_thumbnail_dir + 'Kangaroo_ps.jpg',
            'Lion': image_thumbnail_dir + 'Lion_ps.jpg',
            'Orca': image_thumbnail_dir + 'Orca_ps.jpg',
            'Otter': image_thumbnail_dir + 'Otter_ps.jpg',
            'Owl': image_thumbnail_dir + 'Owl_ps.jpg',
            'Penguin': image_thumbnail_dir + 'Penguin_ps.jpg',
            'Polar Bear': image_thumbnail_dir + 'PolarBear_ps.jpg',
            'Puma': image_thumbnail_dir + 'Puma_ps.jpg',
            'Rabbit': image_thumbnail_dir + 'Rabbit_ps.jpg',
            'Wolf': image_thumbnail_dir + 'Wolf_ps.jpg',
            'Yahweh': image_thumbnail_dir + 'Yahweh_ps.jpg',
        }
        
        message = MessageViewModel(j['SubmittedBy'], j['Message'], j['Mood'], x_date, thumbnail_dict[j['SubmittedBy']])
        message_list.append(message)

    context = {
        'message_list': message_list,
    }
    return render(request, 'messageboard/animal-conversation.html', context)


def add_post(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            z = form.cleaned_data['submitted_by']
            print('====================================')
            print(str(z))
            print('====================================')
            (boto3
                .resource('dynamodb', region_name='us-east-1')
                .Table('PostSomethingAnimalConversations')
                .put_item(
                    Item = {
                        'SubmittedBy': form.cleaned_data['submitted_by'],
                        'Message': form.cleaned_data['message'],
                        'Mood': form.cleaned_data['mood'],
                        'DateTime': str(datetime.datetime.now()),
                    }
                )
            )
            return HttpResponseRedirect('/messageboard/conversation/')
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