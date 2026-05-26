from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('researcher', 'Pesquisador'),
        ('technician', 'Técnico'),
        ('visitor', 'Visitante'),
    ]
    role = models.CharField('Perfil', max_length=20, choices=ROLE_CHOICES, default='visitor')
    phone = models.CharField('Telefone', max_length=20, blank=True)
    institution = models.CharField('Instituição', max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_admin(self): return self.role == 'admin'
    def is_researcher(self): return self.role in ('admin', 'researcher')
    def is_technician(self): return self.role in ('admin', 'technician')

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
