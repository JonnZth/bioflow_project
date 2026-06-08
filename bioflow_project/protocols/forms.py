from django import forms
from .models import Protocolo

class ProtocoloForm(forms.ModelForm):
    class Meta:
        model = Protocolo
        # Definimos quais campos da tabela vão aparecer na tela para o usuário preencher
        fields = ['titulo', 'descricao', 'categoria', 'documento']
        
        # Opcional: Adiciona classes do Bootstrap para ficar bonito depois
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'documento': forms.FileInput(attrs={'class': 'form-control'}),
        }