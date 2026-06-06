from django import forms
from .models import Protocol, ProtocolHistory


class ProtocolForm(forms.ModelForm):
    class Meta:
        model = Protocol
        fields = ['title', 'description', 'category', 'version', 'pdf_file', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'is_active':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProtocolHistoryForm(forms.ModelForm):
    class Meta:
        model = ProtocolHistory
        fields = ['version', 'change_description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
