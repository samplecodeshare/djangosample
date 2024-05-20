from django import forms

class DynamicForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Extract the dynamic fields information from the kwargs
        dynamic_fields = kwargs.pop('dynamic_fields', None)
        super(DynamicForm, self).__init__(*args, **kwargs)

        # If dynamic_fields is provided, dynamically add fields to the form
        if dynamic_fields:
            for field_name, field_options in dynamic_fields.items():
                field_type = field_options.pop('field_type', forms.CharField)
                self.fields[field_name] = field_type(**field_options)

# Usage Example
dynamic_fields = {
    'name': {'field_type': forms.CharField, 'max_length': 50, 'label': 'Your Name'},
    'age': {'field_type': forms.IntegerField, 'min_value': 0, 'max_value': 100, 'label': 'Your Age'},
}

form = DynamicForm(dynamic_fields=dynamic_fields)
