from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from reagents.models import Reagent
from equipments.models import Equipment
from experiments.models import Experiment
from schedules.models import Schedule
from analysis.models import Analysis
from inventory.models import InventoryMovement
import json

@login_required
def index(request):
    today = timezone.now().date()
    # Contadores principais
    active_experiments = Experiment.objects.filter(status='in_progress').count() # Experimentos ativos
    available_equipments = Equipment.objects.filter(status='available').count() # Equipamentos disponíveis
    total_reagents = Reagent.objects.count() 
    today_schedules = Schedule.objects.filter(
        start_datetime__date=today, status='confirmed'
    ).select_related('equipment','user')

    # Alertas de reagentes que estão vencidos, próximos do vencimento ou com estoque baixo, aplicando os metodos ao cehcar
    all_reagents = Reagent.objects.all()
    expired_reagents = [r for r in all_reagents if r.is_expired()]
    expiring_reagents = [r for r in all_reagents if r.is_expiring_soon()]
    low_stock_reagents = [r for r in all_reagents if r.is_low_stock()]

    # Experimentos recentes
    recent_experiments = Experiment.objects.order_by('-created_at')[:5]

    # Chart data — agrupando as análises por tipo
    analysis_by_type = list(
        Analysis.objects.values('analysis_type').annotate(total=Count('id')) #
    )
    chart_labels = [a['analysis_type'] for a in analysis_by_type]
    chart_data = [a['total'] for a in analysis_by_type]

    # Agrupando experimentos por status
    exp_by_status = list(
        Experiment.objects.values('status').annotate(total=Count('id'))
    )

    context = {
        'active_experiments': active_experiments,
        'available_equipments': available_equipments,
        'total_reagents': total_reagents,
        'today_schedules': today_schedules,
        'expired_reagents': expired_reagents[:5],
        'expiring_reagents': expiring_reagents[:5],
        'low_stock_reagents': low_stock_reagents[:5],
        'recent_experiments': recent_experiments,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'exp_by_status': json.dumps([{'status': e['status'], 'total': e['total']} for e in exp_by_status]),
        'total_analyses': Analysis.objects.count(),
        'today': today,
    }
    return render(request, 'dashboard/index.html', context)
