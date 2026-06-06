from django import forms
from .models import Sample, SampleTracking


class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ['code', 'name', 'sample_type', 'origin', 'responsible',
                  'collection_date', 'storage_location', 'storage_details', 'status', 'notes']
        widgets = {
            'collection_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if 'date' not in name:
                field.widget.attrs['class'] = 'form-control'


class SampleTrackingForm(forms.ModelForm):
    class Meta:
        model = SampleTracking
        fields = ['status', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
