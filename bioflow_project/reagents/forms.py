from django import forms
from .models import Reagent
class ReagentForm(forms.ModelForm):
    class Meta:
        model = Reagent
        exclude = ['created_by','created_at','updated_at']
        widgets = {'expiration_date': forms.DateInput(attrs={'type':'date','class':'form-control'})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, f in self.fields.items():
            if name != 'expiration_date':
                f.widget.attrs['class'] = 'form-control'
