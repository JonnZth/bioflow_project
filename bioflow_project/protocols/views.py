from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Protocol
from .forms import ProtocolForm

@login_required
def protocol_list(request):
    q=request.GET.get('q','')
    cat=request.GET.get('category','')
    qs=Protocol.objects.filter(is_active=True)
    if q: qs=qs.filter(title__icontains=q)
    if cat: qs=qs.filter(category=cat)
    return render(request,'protocols/protocol_list.html',{'protocols':qs,'q':q,'category':cat,'categories':Protocol.CATEGORY_CHOICES})

@login_required
def protocol_detail(request,pk):
    p=get_object_or_404(Protocol,pk=pk)
    return render(request,'protocols/protocol_detail.html',{'protocol':p})

@login_required
def protocol_create(request):
    form=ProtocolForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        p=form.save(commit=False);p.author=request.user;p.save()
        messages.success(request,'Protocolo cadastrado!')
        return redirect('protocols:protocol_list')
    return render(request,'protocols/protocol_form.html',{'form':form,'title':'Novo Protocolo'})

@login_required
def protocol_edit(request,pk):
    p=get_object_or_404(Protocol,pk=pk)
    form=ProtocolForm(request.POST or None,request.FILES or None,instance=p)
    if request.method=='POST' and form.is_valid():
        form.save();messages.success(request,'Protocolo atualizado!')
        return redirect('protocols:protocol_detail',pk=pk)
    return render(request,'protocols/protocol_form.html',{'form':form,'title':'Editar Protocolo','protocol':p})
