from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import InventoryMovement
from .forms import MovementForm
from reagents.models import Reagent

@login_required
def movement_list(request):
    qs=InventoryMovement.objects.select_related('reagent','performed_by').order_by('-created_at')
    return render(request,'inventory/movement_list.html',{'movements':qs})

@login_required
def movement_create(request):
    form=MovementForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        m=form.save(commit=False)
        m.performed_by=request.user
        m.previous_quantity=m.reagent.quantity
        try:
            m.full_clean()
            if m.movement_type in ('entry','adjustment'):
                m.new_quantity=m.previous_quantity+m.quantity
            else:
                m.new_quantity=m.previous_quantity-m.quantity
            m.reagent.quantity=m.new_quantity
            m.reagent.save()
            m.save()
            messages.success(request,f'Movimentação registrada. Novo estoque: {m.new_quantity} {m.reagent.unit}')
            return redirect('inventory:movement_list')
        except ValidationError as e:
            messages.error(request,str(e.message))
    return render(request,'inventory/movement_form.html',{'form':form,'title':'Nova Movimentação'})
