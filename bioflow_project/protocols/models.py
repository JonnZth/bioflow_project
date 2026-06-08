from django.db import models

# Tabela para a Categorização
class Categoria(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Categoria")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    def __str__(self):
        return self.nome

# Tabela para o Protocolo (com gerenciamento de documento)
class Protocolo(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título do Protocolo")
    descricao = models.TextField(verbose_name="Descrição Detalhada")
    
    # Faz a ligação com a Categoria
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoria")
    
    # Gerenciamento de documentos associados
    documento = models.FileField(upload_to='documentos_protocolos/', blank=True, null=True, verbose_name="Documento Associado (PDF, DOCX)")
    
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    def __str__(self):
        return self.titulo