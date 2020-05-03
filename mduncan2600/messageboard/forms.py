from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit  # basically, adds a submit button to the form

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=10)


class MessageForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        
        # This is all crispy forms shit
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit('submit', 'Submit'))

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