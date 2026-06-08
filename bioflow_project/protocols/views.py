from django.shortcuts import render, redirect
from .models import Protocolo
from .forms import ProtocoloForm

# 1. CONSULTA (Listar os protocolos cadastrados)
def listar_protocolos(request):
    # Busca todos os protocolos do banco de dados
    protocolos = Protocolo.objects.all().order_by('-data_criacao')
    return render(request, 'protocols/listar.html', {'protocolos': protocolos})

# 2. CADASTRO (Criar um novo protocolo)
def cadastrar_protocolo(request):
    if request.method == 'POST':
        # request.FILES é obrigatório para receber o documento/arquivo anexado
        form = ProtocoloForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() # Salva no banco de dados
            return redirect('listar_protocolos') # Redireciona para a listagem
    else:
        form = ProtocoloForm()
        
    return render(request, 'protocols/cadastrar.html', {'form': form})

# 3. EDIÇÃO (Alterar um protocolo existente)
def editar_protocolo(request, pk):
    # Procura o protocolo que vai ser editado pelo ID (pk)
    protocolo = Protocolo.objects.get(pk=pk)
    
    if request.method == 'POST':
        # Passamos o 'instance=protocolo' para o Django saber que estamos a atualizar e não a criar um novo
        form = ProtocoloForm(request.POST, request.FILES, instance=protocolo)
        if form.is_valid():
            form.save()
            return redirect('listar_protocolos')
    else:
        form = ProtocoloForm(instance=protocolo)
        
    return render(request, 'protocols/cadastrar.html', {'form': form, 'editando': True})