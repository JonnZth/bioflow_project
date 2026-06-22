from django import forms
from .models import Protocol
class ProtocolForm(forms.ModelForm):
    class Meta:
        model=Protocol
        exclude=['author','created_at','updated_at']
    def __init__(self,*a,**k):
        super().__init__(*a,**k)
        for f in self.fields.values():f.widget.attrs['class']='form-control'
