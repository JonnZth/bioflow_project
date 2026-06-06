from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Protocol
from .forms import ProtocolForm


@login_required
def protocol_list(request):
    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    qs = Protocol.objects.select_related('author').all()
    if q:
        qs = qs.filter(title__icontains=q)
    if category:
        qs = qs.filter(category=category)
    return render(request, 'protocols/protocol_list.html', {
        'protocols': qs, 'q': q, 'category': category,
        'categories': Protocol.CATEGORY_CHOICES,
    })


@login_required
def protocol_detail(request, pk):
    protocol = get_object_or_404(Protocol.objects.select_related('author'), pk=pk)
    return render(request, 'protocols/protocol_detail.html', {'protocol': protocol})


@login_required
def protocol_create(request):
    form = ProtocolForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        protocol = form.save(commit=False)
        protocol.author = request.user
        protocol.save()
        messages.success(request, f'Protocolo "{protocol.title}" criado com sucesso!')
        return redirect('protocols:protocol_detail', pk=protocol.pk)
    return render(request, 'protocols/protocol_form.html', {'form': form, 'title': 'Novo Protocolo'})


@login_required
def protocol_edit(request, pk):
    protocol = get_object_or_404(Protocol, pk=pk)
    form = ProtocolForm(request.POST or None, request.FILES or None, instance=protocol)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Protocolo atualizado!')
        return redirect('protocols:protocol_detail', pk=protocol.pk)
    return render(request, 'protocols/protocol_form.html', {
        'form': form, 'title': 'Editar Protocolo', 'protocol': protocol,
    })
