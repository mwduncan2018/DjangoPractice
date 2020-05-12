from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout  # basically, adds a submit button to the form
from crispy_forms.bootstrap import StrictButton, InlineRadios


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=10)


class MessageForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        
        # Crispy-forms configuration
        self.helper = FormHelper()
        self.helper.form_id = 'id-messageForm'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_tag = True
        #self.helper.add_input(Submit('submit', 'Submit'))

        # Crispy-forms Bootstrap3
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            InlineRadios(
                'submitted_by',
                id='radioSubmittedBy'
            ),
            'message',
            InlineRadios(
                'mood',
                id='radioMood'
            ),
            StrictButton(
                content="Submit Message",
                name="btnSubmit",
                type="submit",
                value="Submit Message",
                css_class='btn btn-outline-success my-2 my-sm-0'
            ),
        )

    ANIMAL_CHOICES = (
        ('Bison', 'Bison'),
        ('Black Puma', 'Black Puma'),
        ('Elk', 'Elk'),
        ('Fox', 'Fox'),
        ('Gorilla', 'Gorilla'),
        ('Grizzly', 'Grizzly'),
        ('Hair Bear', 'Hair Bear'),
        ('Kangaroo', 'Kangaroo'),
        ('Lion', 'Lion'),
        ('Orca', 'Orca'),
        ('Otter', 'Otter'),
        ('Owl', 'Owl'),
        ('Penguin', 'Penguin'),
        ('Polar Bear', 'Polar Bear'),
        ('Puma', 'Puma'),
        ('Rabbit', 'Rabbit'),
        ('Wolf', 'Wolf'),
        ('Yahweh', 'Yahweh'),
    )
    submitted_by = forms.ChoiceField(
        label = 'Submitted By',
        choices = ANIMAL_CHOICES,
        required = True,
    )

    MOOD_CHOICES = (
        ('Happy', 'Happy'),
        ('Sad', 'Sad'),
        ('Drunk', 'Drunk'),
        ('Horny', 'Horny'),
        ('Trippin Balls', 'Trippin Balls'),
        ('Angry', 'Angry'),
        ('Violated', 'Violated'),
        ('Excited', 'Excited'),
        ('Depressed', 'Depressed')
    )
    mood = forms.ChoiceField(
        label = 'Mood',
        choices = MOOD_CHOICES,
        required = True,
    )

    message = forms.CharField(
        widget = forms.Textarea,
        label = 'Message',
        max_length = 1000,
    )
    
    send_email = forms.BooleanField(
        label = "Send Email?",
        required = False,
    )
    

class BandForm(forms.Form):
    """Used for practice. Remove whenever you want."""
    
    def __init__(self, *args, **kwargs):
        super(BandForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-bandForm'
        self.helper.form_class = 'yellowForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_bullshit_what_is_going_on'
        self.helper.form_tag = True
        self.helper.add_input(Submit('submit', 'Submit'))
        
    bandName = forms.CharField(
        label = 'Band',
        max_length = 30,
        required = True,
    )
    
    rating = forms.IntegerField(
        label = 'Rating',
        required = False,
    )
    
