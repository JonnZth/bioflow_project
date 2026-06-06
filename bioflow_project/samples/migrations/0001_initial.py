from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Código')),
                ('name', models.CharField(max_length=200, verbose_name='Nome / Descrição')),
                ('sample_type', models.CharField(choices=[('blood', 'Sangue'), ('urine', 'Urina'), ('tissue', 'Tecido'), ('saliva', 'Saliva'), ('dna', 'DNA'), ('rna', 'RNA'), ('other', 'Outro')], default='other', max_length=20, verbose_name='Tipo')),
                ('origin', models.TextField(blank=True, verbose_name='Origem')),
                ('collection_date', models.DateField(verbose_name='Data de Coleta')),
                ('storage_location', models.CharField(choices=[('freezer_20', 'Freezer -20°C'), ('freezer_80', 'Freezer -80°C'), ('fridge_4', 'Geladeira 4°C'), ('room_temp', 'Temperatura Ambiente'), ('other', 'Outro')], default='fridge_4', max_length=20, verbose_name='Local de Armazenamento')),
                ('storage_details', models.CharField(blank=True, max_length=200, verbose_name='Detalhes do Armazenamento')),
                ('status', models.CharField(choices=[('active', 'Ativa'), ('consumed', 'Consumida'), ('discarded', 'Descartada'), ('archived', 'Arquivada')], default='active', max_length=20, verbose_name='Status')),
                ('notes', models.TextField(blank=True, verbose_name='Observações')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='samples_responsible', to=settings.AUTH_USER_MODEL, verbose_name='Responsável')),
            ],
            options={'verbose_name': 'Amostra', 'verbose_name_plural': 'Amostras', 'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='SampleTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('active', 'Ativa'), ('consumed', 'Consumida'), ('discarded', 'Descartada'), ('archived', 'Arquivada')], max_length=20, verbose_name='Status')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Data/Hora')),
                ('notes', models.TextField(blank=True, verbose_name='Observação')),
                ('changed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Responsável')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tracking_events', to='samples.sample', verbose_name='Amostra')),
            ],
            options={'verbose_name': 'Rastreamento', 'verbose_name_plural': 'Rastreamentos', 'ordering': ['timestamp']},
        ),
    ]
