from django import forms
from .models import Experiment
class ExperimentForm(forms.ModelForm):
    class Meta:
        model=Experiment
        exclude=['responsible','created_at','updated_at']
        widgets={
            'start_date':forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'end_date':forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'actual_end_date':forms.DateInput(attrs={'type':'date','class':'form-control'}),
        }
    def __init__(self,*a,**k):
        super().__init__(*a,**k)
        for n,f in self.fields.items():
            if 'date' not in n: f.widget.attrs['class']='form-control'
