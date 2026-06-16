from django import forms
from .models import InventoryMovement
class MovementForm(forms.ModelForm):
    class Meta:
        model=InventoryMovement
        fields=['reagent','movement_type','quantity','reason','experiment']
    def __init__(self,*a,**k):
        super().__init__(*a,**k)
        for f in self.fields.values():f.widget.attrs['class']='form-control'
