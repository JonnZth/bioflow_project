from django.db import models
from django.conf import settings

class Analysis(models.Model):
    TYPE_CHOICES = [
        ('absorbance', 'Absorbância'), ('enzymatic_activity', 'Atividade Enzimática'),
        ('microbial_growth', 'Crescimento Microbiano'), ('concentration', 'Concentração'),
        ('chromatogram', 'Cromatograma'), ('microscopy', 'Microscopia'),
        ('pcr', 'PCR'), ('sequencing', 'Sequenciamento'), ('other', 'Outro'),
    ]
    experiment = models.ForeignKey('experiments.Experiment', on_delete=models.CASCADE, related_name='analyses', verbose_name='Experimento')
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Analista')
    analysis_type = models.CharField('Tipo de Análise', max_length=50, choices=TYPE_CHOICES)
    name = models.CharField('Nome/Identificação', max_length=200)
    description = models.TextField('Descrição Técnica', blank=True)
    numeric_result = models.DecimalField('Resultado Numérico', max_digits=15, decimal_places=4, null=True, blank=True)
    result_unit = models.CharField('Unidade do Resultado', max_length=50, blank=True)
    result_file = models.FileField('Arquivo de Resultado', upload_to='analysis/', null=True, blank=True)
    result_image = models.ImageField('Imagem do Resultado', upload_to='analysis/images/', null=True, blank=True)
    observations = models.TextField('Observações Técnicas', blank=True)
    equipment_used = models.ForeignKey('equipments.Equipment', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Equipamento Utilizado')
    analysis_date = models.DateField('Data da Análise')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Análise'
        verbose_name_plural = 'Análises'
        ordering = ['-analysis_date']

    def __str__(self):
        return f"{self.name} — {self.experiment.title}"
