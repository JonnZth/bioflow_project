from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Schedule
from .forms import ScheduleForm

@login_required
def schedule_list(request):
    qs=Schedule.objects.select_related('equipment','user').order_by('start_datetime')
    eq=request.GET.get('equipment','')
    if eq: qs=qs.filter(equipment__name__icontains=eq)
    return render(request,'schedules/schedule_list.html',{'schedules':qs,'equipment':eq})

@login_required
def schedule_create(request):
    form=ScheduleForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        s=form.save(commit=False); s.user=request.user
        try:
            s.full_clean(); s.save()
            messages.success(request,'Agendamento realizado!')
            return redirect('schedules:schedule_list')
        except ValidationError as e:
            messages.error(request,str(e.message))
    return render(request,'schedules/schedule_form.html',{'form':form,'title':'Novo Agendamento'})

@login_required
def schedule_cancel(request,pk):
    s=get_object_or_404(Schedule,pk=pk,user=request.user)
    if request.method=='POST':
        s.status='cancelled'; s.save()
        messages.info(request,'Agendamento cancelado.')
        return redirect('schedules:schedule_list')
    return render(request,'schedules/schedule_confirm_cancel.html',{'schedule':s})
