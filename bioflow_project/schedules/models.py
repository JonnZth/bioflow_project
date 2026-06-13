from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Schedule(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('confirmed', 'Confirmado'),
        ('cancelled', 'Cancelado'),
        ('completed', 'Concluído'),
    ]
    equipment = models.ForeignKey('equipments.Equipment', on_delete=models.CASCADE, related_name='schedules', verbose_name='Equipamento')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuário')
    start_datetime = models.DateTimeField('Início')
    end_datetime = models.DateTimeField('Fim')
    purpose = models.TextField('Finalidade')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='confirmed')
    notes = models.TextField('Observações', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.start_datetime and self.end_datetime:
            if self.end_datetime <= self.start_datetime:
                raise ValidationError('A data de fim deve ser após o início.')
            conflicts = Schedule.objects.filter(
                equipment=self.equipment,
                status__in=['pending', 'confirmed'],
                start_datetime__lt=self.end_datetime,
                end_datetime__gt=self.start_datetime,
            ).exclude(pk=self.pk)
            if conflicts.exists():
                raise ValidationError(f'Conflito de agendamento! Equipamento reservado nesse período.')

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['start_datetime']

    def __str__(self):
        return f"{self.equipment.name} — {self.user.username} ({self.start_datetime.strftime('%d/%m/%Y %H:%M')})"
