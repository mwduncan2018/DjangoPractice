import time
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


def add_post(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
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
            return HttpResponseRedirect('/postsomething/chat/')
    else:
        message_form = MessageForm()
        context = {
            'message_form': message_form,
        }
        return render(request, 'messageboard/add-post.html', context)


def clear_conversation(request):
    if request.method == 'POST':
        
        # Delete the table 
        (boto3
            .resource('dynamodb', region_name='us-east-1')
            .Table('PostSomethingAnimalConversations')
            .delete()
        )
        time.sleep(5)  # Wait 5 seconds for the table to delete

        # Create the table
        (boto3
            .resource('dynamodb', region_name='us-east-1')
            .create_table(
                TableName = 'PostSomethingAnimalConversations',
                KeySchema = [
                    {
                        'AttributeName': 'SubmittedBy',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'DateTime',
                        'KeyType': 'RANGE'
                    }
                ],
                AttributeDefinitions = [
                    {
                        'AttributeName': 'SubmittedBy',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'DateTime',
                        'AttributeType': 'S'
                    },
                ],
                ProvisionedThroughput = {
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
        )
        time.sleep(10)  # Wait 5 seconds for the table to be created
        
        return HttpResponseRedirect('/postsomething/chat/')
    else:
        return render(request, 'messageboard/clear-conversation.html')


def splash(request):
    return HttpResponse("Du!")


def animal_conversation(request):
    class AnimalConversationViewModel:
        def __init__(self, submitted_by=None, message=None, mood=None, datetime=None, picture=None):
            self.id = id
            self.submitted_by = submitted_by
            self.message = message
            self.mood = mood
            self.datetime = datetime
            self.picture = picture
        def __str__(self):
            return str(self.message) + " (" + str(self.submitted_by) + ")"
    
    image_dir = '/static/messageboard/images/thumbnails/'
    thumbnail_dict = {
        'Bison': image_dir + 'Bison_ps.jpg',
        'Black Puma': image_dir + 'BlackPanther_ps.jpg',
        'Elk': image_dir + 'Elk_ps.jpg',
        'Fox': image_dir + 'Fox_ps.jpg',
        'Gorilla': image_dir + 'Gorilla_ps.jpg',
        'Grizzly': image_dir + 'Grizzly_ps.jpg',
        'Hair Bear': image_dir + 'HairBear_ps.jpg',
        'Kangaroo': image_dir + 'Kangaroo_ps.jpg',
        'Lion': image_dir + 'Lion_ps.jpg',
        'Orca': image_dir + 'Orca_ps.jpg',
        'Otter': image_dir + 'Otter_ps.jpg',
        'Owl': image_dir + 'Owl_ps.jpg',
        'Penguin': image_dir + 'Penguin_ps.jpg',
        'Polar Bear': image_dir + 'PolarBear_ps.jpg',
        'Puma': image_dir + 'Puma_ps.jpg',
        'Rabbit': image_dir + 'Rabbit_ps.jpg',
        'Wolf': image_dir + 'Wolf_ps.jpg',
        'Yahweh': image_dir + 'Yahweh_ps.jpg',
    }

    # Get the data from AWS DynamoDB
    response = (boto3
        .resource('dynamodb', region_name='us-east-1')
        .Table('PostSomethingAnimalConversations')
        .scan())

    # Put the data in a List of MessageViewModel
    message_list = []
    for j in response['Items']:
        x_date = datetime.datetime.strptime(j['DateTime'], '%Y-%m-%d %H:%M:%S.%f')
        message = AnimalConversationViewModel(j['SubmittedBy'], j['Message'], j['Mood'], x_date, thumbnail_dict[j['SubmittedBy']])
        message_list.append(message)
    message_list.sort(key=lambda x: x.datetime, reverse=True)
    
    context = {
        'message_list': message_list,
    }
    return render(request, 'messageboard/animal-conversation.html', context)


def view_animals(request):
    class ViewAnimalsViewModel:
        def __init__(self, name=None, picture=None, title=None, info=None, link=None):
            self.name = name
            self.picture = picture
            self.title = title
            self.info = info
            self.link = link
        def __str__(self):
            return " - ".join([str(self.name), str(self.link)])

    image_dir = '/static/messageboard/images/cards/'
    cards_dict = {
        'Bison': image_dir + 'Bison_ps.jpg',
        'Black Panther': image_dir + 'BlackPanther_ps.jpg',
        'Elk': image_dir + 'Elk_ps.jpg',
        'Fox': image_dir + 'Fox_ps.jpg',
        'Gorilla': image_dir + 'Gorilla_ps.jpg',
        'Grizzly': image_dir + 'Grizzly_ps.jpg',
        'Hair Bear': image_dir + 'HairBear_ps.jpg',
        'Kangaroo': image_dir + 'Kangaroo_ps.jpg',
        'Lion': image_dir + 'Lion_ps.jpg',
        'Orca': image_dir + 'Orca_ps.jpg',
        'Otter': image_dir + 'Otter_ps.jpg',
        'Owl': image_dir + 'Owl_ps.jpg',
        'Penguin': image_dir + 'Penguin_ps.jpg',
        'Polar Bear': image_dir + 'PolarBear_ps.jpg',
        'Puma': image_dir + 'Puma_ps.jpg',
        'Rabbit': image_dir + 'Rabbit_ps.jpg',
        'Wolf': image_dir + 'Wolf_ps.jpg',
        'Yahweh': image_dir + 'Yahweh_ps.jpg',
    }

    card_list = []
    card_list.append(ViewAnimalsViewModel('Bison', cards_dict['Bison'], 'North American Herbivore', '50+ million killed in the 1800s', 'https://en.wikipedia.org/wiki/Bison'))
    card_list.append(ViewAnimalsViewModel('Black Panther', cards_dict['Black Panther'], 'Carnivore', 'Common in equatorial rainforest', 'https://en.wikipedia.org/wiki/Black_panther'))
    card_list.append(ViewAnimalsViewModel('Elk', cards_dict['Elk'], 'North American Herbivore', 'Hunted by wolves', 'https://en.wikipedia.org/wiki/Elk'))
    card_list.append(ViewAnimalsViewModel('Fox', cards_dict['Fox'], 'Omnivorous Mammal', 'Prominent in popular folklore', 'https://en.wikipedia.org/wiki/Fox'))
    card_list.append(ViewAnimalsViewModel('Grizzly', cards_dict['Grizzly'], 'North American Carnivore', 'Most reside in Alaksa', 'https://en.wikipedia.org/wiki/Grizzly_bear'))
    card_list.append(ViewAnimalsViewModel('Hair Bear', cards_dict['Hair Bear'], 'Domestic Cat', 'Most active dawn to dusk', 'https://en.wikipedia.org/wiki/Persian_cat'))
    card_list.append(ViewAnimalsViewModel('Kangaroo', cards_dict['Kangaroo'], 'Marsupial', 'A symbol of Australia', 'https://en.wikipedia.org/wiki/Kangaroo'))
    card_list.append(ViewAnimalsViewModel('Lion', cards_dict['Lion'], 'Keystone Predator', 'Lives in a pride', 'https://en.wikipedia.org/wiki/Lion'))
    card_list.append(ViewAnimalsViewModel('Orca', cards_dict['Orca'], 'Apex Predator', 'Kills trainers at Sea World', 'https://en.wikipedia.org/wiki/Killer_whale'))
    card_list.append(ViewAnimalsViewModel('Otter', cards_dict['Otter'], 'Semiaquatic', 'Related to wolverines', 'https://en.wikipedia.org/wiki/Otter'))
    card_list.append(ViewAnimalsViewModel('Owl', cards_dict['Owl'], 'Nocturnal Bird of Prey', 'Reverse sexual dimorphism', 'https://en.wikipedia.org/wiki/Owl'))
    card_list.append(ViewAnimalsViewModel('Penguin', cards_dict['Penguin'], 'Southern Hemisphere', 'Flightless bird', 'https://en.wikipedia.org/wiki/Penguin'))
    card_list.append(ViewAnimalsViewModel('Polar Bear', cards_dict['Polar Bear'], 'Arctic Predator', 'Largest land carnivore', 'https://en.wikipedia.org/wiki/Polar_bear'))
    card_list.append(ViewAnimalsViewModel('Puma', cards_dict['Puma'], 'American Carnivore', 'Ambush predator', 'https://en.wikipedia.org/wiki/Cougar'))
    card_list.append(ViewAnimalsViewModel('Rabbit', cards_dict['Rabbit'], 'Small Herbivore', 'Owl food', 'https://en.wikipedia.org/wiki/Rabbit'))
    card_list.append(ViewAnimalsViewModel('Wolf', cards_dict['Wolf'], 'Territorial Carnivore', 'Highly social behavior', 'https://en.wikipedia.org/wiki/Wolf'))
    card_list.append(ViewAnimalsViewModel('Yahweh', cards_dict['Yahweh'], 'Universe Creator', 'Surprise bitch! I\'m real!', 'https://www.youtube.com/watch?v=Z1BzP1wr234'))

    context = {
        'card_list': card_list,
    }
    return render(request, 'messageboard/view-animals.html', context)
    
    
def about(request):
    context = {
        'message': 'hey delete page',
    }
    return render(request, 'messageboard/about.html', context)