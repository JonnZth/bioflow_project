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
            name='Protocol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título')),
                ('description', models.TextField(blank=True, verbose_name='Descrição')),
                ('category', models.CharField(choices=[('extraction', 'Extração'), ('purification', 'Purificação'), ('amplification', 'Amplificação'), ('sequencing', 'Sequenciamento'), ('culture', 'Cultivo'), ('analysis', 'Análise'), ('other', 'Outro')], default='other', max_length=30, verbose_name='Categoria')),
                ('version', models.CharField(default='1.0', max_length=20, verbose_name='Versão')),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='protocols/', verbose_name='Arquivo PDF')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='protocols_authored', to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
            ],
            options={'verbose_name': 'Protocolo', 'verbose_name_plural': 'Protocolos', 'ordering': ['title']},
        ),
        migrations.CreateModel(
            name='ProtocolHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=20, verbose_name='Versão')),
                ('change_description', models.TextField(verbose_name='Descrição da Alteração')),
                ('changed_at', models.DateTimeField(auto_now_add=True, verbose_name='Data')),
                ('changed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Alterado por')),
                ('protocol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='protocols.protocol', verbose_name='Protocolo')),
            ],
            options={'verbose_name': 'Histórico de Protocolo', 'verbose_name_plural': 'Histórico de Protocolos', 'ordering': ['-changed_at']},
        ),
    ]
