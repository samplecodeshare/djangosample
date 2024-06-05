from django import forms

class InputForm(forms.Form):
    INPUT_TYPES = [
        ('sql', 'SQL'),
        ('json', 'JSON'),
        ('xml', 'XML')
    ]
    input_type = forms.ChoiceField(choices=INPUT_TYPES, required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)
