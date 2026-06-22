from django.db import models
from django.conf import settings

class Protocol(models.Model):
    CATEGORY_CHOICES = [
        ('fermentation', 'Fermentação'), ('pcr', 'PCR'),
        ('extraction', 'Extração'), ('chromatography', 'Cromatografia'),
        ('microscopy', 'Microscopia'), ('cell_culture', 'Cultura de Células'),
        ('enzymatic', 'Enzimático'), ('other', 'Outro'),
    ]
    title = models.CharField('Título', max_length=300)
    category = models.CharField('Categoria', max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField('Descrição')
    pdf_file = models.FileField('Arquivo PDF', upload_to='protocols/', null=True, blank=True)
    version = models.CharField('Versão', max_length=20, default='1.0')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Autor')
    is_active = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Protocolo'
        verbose_name_plural = 'Protocolos'
        ordering = ['title']

    def __str__(self):
        return f"{self.title} (v{self.version})"

class ProtocolHistory(models.Model):
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE, related_name='history')
    version = models.CharField('Versão', max_length=20)
    change_description = models.TextField('Descrição da Alteração')
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-changed_at']
