from django.db import models
from django.conf import settings


class Protocol(models.Model):
    CATEGORY_CHOICES = [
        ('extraction', 'Extração'),
        ('purification', 'Purificação'),
        ('amplification', 'Amplificação'),
        ('sequencing', 'Sequenciamento'),
        ('culture', 'Cultivo'),
        ('analysis', 'Análise'),
        ('other', 'Outro'),
    ]

    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição', blank=True)
    category = models.CharField('Categoria', max_length=30, choices=CATEGORY_CHOICES, default='other')
    version = models.CharField('Versão', max_length=20, default='1.0')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='protocols_authored',
        verbose_name='Autor'
    )
    pdf_file = models.FileField('Arquivo PDF', upload_to='protocols/', null=True, blank=True)
    is_active = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Protocolo'
        verbose_name_plural = 'Protocolos'
        ordering = ['title']

    def __str__(self):
        return f'{self.title} (v{self.version})'


class ProtocolHistory(models.Model):
    protocol = models.ForeignKey(
        Protocol, on_delete=models.CASCADE,
        related_name='history', verbose_name='Protocolo'
    )
    version = models.CharField('Versão', max_length=20)
    change_description = models.TextField('Descrição da Alteração')
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, verbose_name='Alterado por'
    )
    changed_at = models.DateTimeField('Data', auto_now_add=True)

    class Meta:
        verbose_name = 'Histórico de Protocolo'
        verbose_name_plural = 'Histórico de Protocolos'
        ordering = ['-changed_at']

    def __str__(self):
        return f'{self.protocol.title} v{self.version}'
