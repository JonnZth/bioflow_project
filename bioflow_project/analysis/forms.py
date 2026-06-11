from django import forms
from .models import Analysis
class AnalysisForm(forms.ModelForm):
    class Meta:
        model=Analysis
        exclude=['analyst','created_at']
        widgets={'analysis_date':forms.DateInput(attrs={'type':'date','class':'form-control'})}
    def __init__(self,*a,**k):
        super().__init__(*a,**k)
        for n,f in self.fields.items():
            if n!='analysis_date': f.widget.attrs['class']='form-control'
