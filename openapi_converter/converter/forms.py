from django import forms

class InputForm(forms.Form):
    INPUT_TYPES = [
        ('sql', 'SQL'),
        ('json', 'JSON'),
        ('xml', 'XML')
    ]
    input_type = forms.ChoiceField(choices=INPUT_TYPES, required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)

class OpenAPIGeneratorForm(forms.Form):
    INPUT_CHOICES = [
        ('json', 'Sample JSON'),
        ('sql', 'SQL Query'),
    ]
    input_type = forms.ChoiceField(choices=INPUT_CHOICES, required=True)
    json_sample = forms.CharField(widget=forms.Textarea, required=False)
    connection_string = forms.CharField(required=False)
    user_id = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    sql_query = forms.CharField(widget=forms.Textarea, required=False)
