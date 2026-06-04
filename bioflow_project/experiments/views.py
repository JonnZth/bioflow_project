from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Experiment
from .forms import ExperimentForm

@login_required
def experiment_list(request):
    q=request.GET.get('q','')
    st=request.GET.get('status','')
    qs=Experiment.objects.all()
    if q: qs=qs.filter(title__icontains=q)
    if st: qs=qs.filter(status=st)
    return render(request,'experiments/experiment_list.html',{'experiments':qs,'q':q,'status':st,'status_choices':Experiment.STATUS_CHOICES})

@login_required
def experiment_detail(request,pk):
    e=get_object_or_404(Experiment,pk=pk)
    analyses=e.analyses.all()
    return render(request,'experiments/experiment_detail.html',{'experiment':e,'analyses':analyses})

@login_required
def experiment_create(request):
    form=ExperimentForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        e=form.save(commit=False);e.responsible=request.user;e.save();form.save_m2m()
        messages.success(request,'Experimento criado!')
        return redirect('experiments:experiment_detail',pk=e.pk)
    return render(request,'experiments/experiment_form.html',{'form':form,'title':'Novo Experimento'})

@login_required
def experiment_edit(request,pk):
    e=get_object_or_404(Experiment,pk=pk)
    form=ExperimentForm(request.POST or None,request.FILES or None,instance=e)
    if request.method=='POST' and form.is_valid():
        form.save();messages.success(request,'Experimento atualizado!')
        return redirect('experiments:experiment_detail',pk=pk)
    return render(request,'experiments/experiment_form.html',{'form':form,'title':'Editar Experimento','experiment':e})
