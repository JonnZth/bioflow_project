from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class InventoryMovement(models.Model):
    TYPE_CHOICES = [
        ('entry', 'Entrada'), ('exit', 'Saída'), ('adjustment', 'Ajuste'), ('loss', 'Descarte'),
    ]
    reagent = models.ForeignKey('reagents.Reagent', on_delete=models.CASCADE, related_name='movements', verbose_name='Reagente')
    movement_type = models.CharField('Tipo', max_length=20, choices=TYPE_CHOICES)
    quantity = models.DecimalField('Quantidade', max_digits=10, decimal_places=2)
    previous_quantity = models.DecimalField('Quantidade Anterior', max_digits=10, decimal_places=2)
    new_quantity = models.DecimalField('Nova Quantidade', max_digits=10, decimal_places=2)
    reason = models.TextField('Motivo', blank=True)
    experiment = models.ForeignKey('experiments.Experiment', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Experimento Associado')
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Realizado por')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.movement_type == 'exit' and self.reagent:
            if self.quantity > self.reagent.quantity:
                raise ValidationError('Quantidade insuficiente em estoque!')

    class Meta:
        verbose_name = 'Movimentação de Estoque'
        verbose_name_plural = 'Movimentações de Estoque'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_movement_type_display()} — {self.reagent.name} ({self.quantity} {self.reagent.unit})"
