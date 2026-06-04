from django.db import models
from django.conf import settings

class Experiment(models.Model):
    STATUS_CHOICES = [
        ('planning', 'Planejamento'), ('in_progress', 'Em Andamento'),
        ('paused', 'Pausado'), ('completed', 'Concluído'), ('cancelled', 'Cancelado'),
    ]
    title = models.CharField('Título', max_length=300)
    description = models.TextField('Descrição')
    hypothesis = models.TextField('Hipótese', blank=True)
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='experiments_responsible', verbose_name='Responsável')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='experiments_participant', verbose_name='Participantes')
    protocol = models.ForeignKey('protocols.Protocol', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Protocolo')
    reagents = models.ManyToManyField('reagents.Reagent', blank=True, verbose_name='Reagentes')
    samples = models.ManyToManyField('samples.Sample', blank=True, verbose_name='Amostras')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='planning')
    start_date = models.DateField('Início')
    end_date = models.DateField('Fim Previsto', null=True, blank=True)
    actual_end_date = models.DateField('Fim Real', null=True, blank=True)
    results_summary = models.TextField('Resumo dos Resultados', blank=True)
    conclusions = models.TextField('Conclusões', blank=True)
    attachment = models.FileField('Anexo', upload_to='experiments/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Experimento'
        verbose_name_plural = 'Experimentos'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
