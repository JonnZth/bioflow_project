from django.db import models
from django.conf import settings


class Sample(models.Model):
    STATUS_CHOICES = [
        ('active', 'Ativa'),
        ('consumed', 'Consumida'),
        ('discarded', 'Descartada'),
        ('archived', 'Arquivada'),
    ]
    TYPE_CHOICES = [
        ('blood', 'Sangue'),
        ('urine', 'Urina'),
        ('tissue', 'Tecido'),
        ('saliva', 'Saliva'),
        ('dna', 'DNA'),
        ('rna', 'RNA'),
        ('other', 'Outro'),
    ]
    STORAGE_CHOICES = [
        ('freezer_20', 'Freezer -20°C'),
        ('freezer_80', 'Freezer -80°C'),
        ('fridge_4', 'Geladeira 4°C'),
        ('room_temp', 'Temperatura Ambiente'),
        ('other', 'Outro'),
    ]

    code = models.CharField('Código', max_length=50, unique=True)
    name = models.CharField('Nome / Descrição', max_length=200)
    sample_type = models.CharField('Tipo', max_length=20, choices=TYPE_CHOICES, default='other')
    origin = models.TextField('Origem', blank=True)
    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='samples_responsible',
        verbose_name='Responsável'
    )
    collection_date = models.DateField('Data de Coleta')
    storage_location = models.CharField('Local de Armazenamento', max_length=20, choices=STORAGE_CHOICES, default='fridge_4')
    storage_details = models.CharField('Detalhes do Armazenamento', max_length=200, blank=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='active')
    notes = models.TextField('Observações', blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Amostra'
        verbose_name_plural = 'Amostras'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.code} – {self.name}'


class SampleTracking(models.Model):
    sample = models.ForeignKey(
        Sample, on_delete=models.CASCADE,
        related_name='tracking_events', verbose_name='Amostra'
    )
    status = models.CharField('Status', max_length=20, choices=Sample.STATUS_CHOICES)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, verbose_name='Responsável'
    )
    timestamp = models.DateTimeField('Data/Hora', auto_now_add=True)
    notes = models.TextField('Observação', blank=True)

    class Meta:
        verbose_name = 'Rastreamento'
        verbose_name_plural = 'Rastreamentos'
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.sample.code} → {self.get_status_display()} em {self.timestamp:%d/%m/%Y %H:%M}'
