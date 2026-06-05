from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Schedule
from .forms import ScheduleForm


@login_required
def schedule_list(request):
    schedules = Schedule.objects.all()

    return render(
        request,
        'schedules/schedule_list.html',
        {'schedules': schedules}
    )


@login_required
def schedule_create(request):

    if request.method == 'POST':
        form = ScheduleForm(request.POST)

        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = request.user
            schedule.save()

            messages.success(
                request,
                'Agendamento criado com sucesso.'
            )

            return redirect('schedule_list')

    else:
        form = ScheduleForm()

    return render(
        request,
        'schedules/schedule_form.html',
        {'form': form}
    )


@login_required
def schedule_detail(request, pk):

    schedule = get_object_or_404(
        Schedule,
        pk=pk
    )

    return render(
        request,
        'schedules/schedule_detail.html',
        {'schedule': schedule}
    )


@login_required
def schedule_delete(request, pk):

    schedule = get_object_or_404(
        Schedule,
        pk=pk
    )

    if request.method == 'POST':
        schedule.delete()

        messages.success(
            request,
            'Agendamento removido com sucesso.'
        )

        return redirect('schedule_list')

    return render(
        request,
        'schedules/schedule_delete.html',
        {'schedule': schedule}
    )
