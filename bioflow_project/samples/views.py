from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Sample, SampleTracking
from .forms import SampleForm, SampleTrackingForm


@login_required
def sample_list(request):
    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    qs = Sample.objects.select_related('responsible').all()
    if q:
        qs = qs.filter(name__icontains=q) | qs.filter(code__icontains=q)
    if status:
        qs = qs.filter(status=status)
    return render(request, 'samples/sample_list.html', {
        'samples': qs, 'q': q, 'status': status,
        'status_choices': Sample.STATUS_CHOICES,
    })


@login_required
def sample_detail(request, pk):
    sample = get_object_or_404(Sample.objects.select_related('responsible'), pk=pk)
    tracking = sample.tracking_events.select_related('changed_by').all()
    tracking_form = SampleTrackingForm()
    return render(request, 'samples/sample_detail.html', {
        'sample': sample,
        'tracking': tracking,
        'tracking_form': tracking_form,
    })


@login_required
def sample_create(request):
    form = SampleForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        sample = form.save()
        SampleTracking.objects.create(
            sample=sample, status=sample.status,
            changed_by=request.user, notes='Amostra registrada no sistema.',
        )
        messages.success(request, f'Amostra {sample.code} registrada com sucesso!')
        return redirect('samples:sample_detail', pk=sample.pk)
    return render(request, 'samples/sample_form.html', {'form': form, 'title': 'Nova Amostra'})


@login_required
def sample_edit(request, pk):
    sample = get_object_or_404(Sample, pk=pk)
    form = SampleForm(request.POST or None, instance=sample)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Amostra atualizada!')
        return redirect('samples:sample_detail', pk=sample.pk)
    return render(request, 'samples/sample_form.html', {
        'form': form, 'title': 'Editar Amostra', 'sample': sample,
    })


@login_required
def sample_update_status(request, pk):
    sample = get_object_or_404(Sample, pk=pk)
    if request.method == 'POST':
        form = SampleTrackingForm(request.POST)
        if form.is_valid():
            sample.status = form.cleaned_data['status']
            sample.save(update_fields=['status', 'updated_at'])
            SampleTracking.objects.create(
                sample=sample,
                status=form.cleaned_data['status'],
                changed_by=request.user,
                notes=form.cleaned_data.get('notes', ''),
            )
            messages.success(request, 'Status atualizado com rastreabilidade registrada.')
    return redirect('samples:sample_detail', pk=sample.pk)
