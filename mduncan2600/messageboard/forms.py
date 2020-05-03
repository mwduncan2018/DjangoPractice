from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout  # basically, adds a submit button to the form
from crispy_forms.bootstrap import StrictButton

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=10)


class MessageForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        
        # Crispy-forms configuration
        self.helper = FormHelper()
        self.helper.form_id = 'id-messageForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.form_tag = True
        #self.helper.add_input(Submit('submit', 'Submit'))

        # Crispy-forms Bootstrap3
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'submitted_by',
            'message',
            'i_am_gay',
            StrictButton(
                content="Submit Message",
                name="btnSubmit",
                type="submit",
                value="Submit Message",
                css_class='btn-default'
            ),
        )

    submitted_by = forms.CharField(
        label = 'Submitted by Animal',
        max_length = 20,
        required = True,
    )

    message = forms.CharField(
        widget = forms.Textarea,
        label = 'Message',
        max_length = 1000,
    )
    
    i_am_gay = forms.BooleanField(
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
    
