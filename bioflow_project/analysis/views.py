from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Analysis
from .forms import AnalysisForm

@login_required
def analysis_list(request):
    qs=Analysis.objects.select_related('experiment','analyst')
    t=request.GET.get('type','')
    if t: qs=qs.filter(analysis_type=t)
    return render(request,'analysis/analysis_list.html',{'analyses':qs,'type':t,'type_choices':Analysis.TYPE_CHOICES})

@login_required
def analysis_detail(request,pk):
    a=get_object_or_404(Analysis,pk=pk)
    return render(request,'analysis/analysis_detail.html',{'analysis':a})

@login_required
def analysis_create(request):
    form=AnalysisForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        a=form.save(commit=False);a.analyst=request.user;a.save()
        messages.success(request,'Análise registrada!')
        return redirect('analysis:analysis_detail',pk=a.pk)
    return render(request,'analysis/analysis_form.html',{'form':form,'title':'Nova Análise'})
