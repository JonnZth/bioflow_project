from django import forms
from .models import Schedule
class ScheduleForm(forms.ModelForm):
    class Meta:
        model=Schedule
        fields=['equipment','start_datetime','end_datetime','purpose','notes']
        widgets={
            'start_datetime':forms.DateTimeInput(attrs={'type':'datetime-local','class':'form-control'}),
            'end_datetime':forms.DateTimeInput(attrs={'type':'datetime-local','class':'form-control'}),
        }
    def __init__(self,*a,**k):
        super().__init__(*a,**k)
        for n,f in self.fields.items():
            if 'datetime' not in n: f.widget.attrs['class']='form-control'
