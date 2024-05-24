from django import forms
import yaml

class YamlForm(forms.Form):
    yaml_content = forms.CharField(widget=forms.Textarea, label='YAML Content')

    def clean_yaml_content(self):
        data = self.cleaned_data['yaml_content']
        try:
            yaml.safe_load(data)
        except yaml.YAMLError as e:
            raise forms.ValidationError(f"Invalid YAML content: {e}")
        return data
