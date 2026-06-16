from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Reagent
from .forms import ReagentForm

@login_required
def reagent_list(request):
    q = request.GET.get('q','')
    cat = request.GET.get('category','')
    alert = request.GET.get('alert','')
    qs = Reagent.objects.all()
    if q: qs = qs.filter(Q(name__icontains=q)|Q(lot__icontains=q)|Q(supplier__icontains=q))
    if cat: qs = qs.filter(category=cat)
    today = timezone.now().date()
    expired = [r.pk for r in qs if r.is_expired()]
    expiring = [r.pk for r in qs if r.is_expiring_soon()]
    low = [r.pk for r in qs if r.is_low_stock()]
    if alert == 'expired': qs = qs.filter(pk__in=expired)
    elif alert == 'expiring': qs = qs.filter(pk__in=expiring)
    elif alert == 'low': qs = qs.filter(pk__in=low)
    return render(request, 'reagents/reagent_list.html', {
        'reagents': qs, 'q': q, 'category': cat, 'alert': alert,
        'expired_count': len(expired), 'expiring_count': len(expiring), 'low_count': len(low),
        'categories': Reagent.CATEGORY_CHOICES,
    })

@login_required
def reagent_detail(request, pk):
    reagent = get_object_or_404(Reagent, pk=pk)
    movements = reagent.movements.all()[:10]
    return render(request, 'reagents/reagent_detail.html', {'reagent': reagent, 'movements': movements})

@login_required
def reagent_create(request):
    form = ReagentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        r = form.save(commit=False)
        r.created_by = request.user
        r.save()
        messages.success(request, f'Reagente "{r.name}" cadastrado com sucesso!')
        return redirect('reagents:reagent_list')
    return render(request, 'reagents/reagent_form.html', {'form': form, 'title': 'Novo Reagente'})

@login_required
def reagent_edit(request, pk):
    reagent = get_object_or_404(Reagent, pk=pk)
    form = ReagentForm(request.POST or None, instance=reagent)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Reagente atualizado!')
        return redirect('reagents:reagent_detail', pk=pk)
    return render(request, 'reagents/reagent_form.html', {'form': form, 'title': 'Editar Reagente', 'reagent': reagent})

@login_required
def reagent_delete(request, pk):
    reagent = get_object_or_404(Reagent, pk=pk)
    if request.method == 'POST':
        reagent.delete()
        messages.success(request, 'Reagente excluído.')
        return redirect('reagents:reagent_list')
    return render(request, 'reagents/reagent_confirm_delete.html', {'reagent': reagent})
