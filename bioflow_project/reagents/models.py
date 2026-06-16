from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

class Reagent(models.Model):
    CATEGORY_CHOICES = [
        ('solvent', 'Solvente'), ('acid', 'Ácido'), ('base', 'Base'),
        ('salt', 'Sal'), ('buffer', 'Tampão'), ('enzyme', 'Enzima'),
        ('antibody', 'Anticorpo'), ('culture_media', 'Meio de Cultura'),
        ('dye', 'Corante'), ('other', 'Outro'),
    ]
    name = models.CharField('Nome', max_length=200)
    category = models.CharField('Categoria', max_length=50, choices=CATEGORY_CHOICES)
    manufacturer = models.CharField('Fabricante', max_length=200)
    lot = models.CharField('Lote', max_length=100)
    expiration_date = models.DateField('Data de Validade')
    quantity = models.DecimalField('Quantidade', max_digits=10, decimal_places=2)
    unit = models.CharField('Unidade', max_length=20)
    supplier = models.CharField('Fornecedor', max_length=200)
    location = models.CharField('Localização', max_length=200)
    cas_number = models.CharField('Número CAS', max_length=50, blank=True)
    safety_notes = models.TextField('Notas de Segurança', blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Cadastrado por')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        return self.expiration_date < timezone.now().date()

    def is_expiring_soon(self):
        return self.expiration_date <= (timezone.now().date() + timedelta(days=settings.EXPIRY_ALERT_DAYS)) and not self.is_expired()

    def is_low_stock(self):
        return self.quantity <= settings.LOW_STOCK_THRESHOLD

    class Meta:
        verbose_name = 'Reagente'
        verbose_name_plural = 'Reagentes'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (Lote: {self.lot})"
