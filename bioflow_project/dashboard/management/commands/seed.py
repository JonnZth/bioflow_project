# -*- coding: utf-8 -*-
import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta
from reagents.models import Reagent
from equipments.models import Equipment, EquipmentFailure
from protocols.models import Protocol
from experiments.models import Experiment
from samples.models import Sample
from analysis.models import Analysis
from schedules.models import Schedule
from inventory.models import InventoryMovement

User = get_user_model()


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de demonstracao do BioFlow'

    def handle(self, *args, **kwargs):
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING(
                'Dados ja existem. Delete o db.sqlite3 e rode novamente.'
            ))
            return

        self._criar_usuarios()
        self._criar_reagentes()
        self._criar_equipamentos()
        self._criar_protocolos()
        self._criar_amostras()
        self._criar_experimentos()
        self._criar_analises()
        self._criar_agendamentos()
        self._criar_movimentacoes()
        self._resumo()

    def _criar_usuarios(self):
        User = get_user_model()
        self.admin  = User.objects.create_superuser('admin',      'admin@bioflow.com',  'admin123', role='admin',       first_name='Adejanildo',   last_name='Pereira',    institution='UVA')
        self.res1   = User.objects.create_user(    'ana.costa',   'ana@bioflow.com',    'bio2026',  role='researcher',  first_name='Ana',      last_name='Costa',    institution='UFRJ')
        self.res2   = User.objects.create_user(    'marcos.lima', 'marcos@bioflow.com', 'bio2026',  role='researcher',  first_name='Marcos',   last_name='Lima',     institution='UFRJ')
        self.res3   = User.objects.create_user(    'julia.reis',  'julia@bioflow.com',  'bio2026',  role='researcher',  first_name='Julia',    last_name='Reis',     institution='UERJ')
        self.tech1  = User.objects.create_user(    'tecnico1',    'tec1@bioflow.com',   'bio2026',  role='technician',  first_name='Joao',     last_name='Mendes',   institution='UFRJ')
        self.tech2  = User.objects.create_user(    'tecnico2',    'tec2@bioflow.com',   'bio2026',  role='technician',  first_name='Fernanda', last_name='Souza',    institution='UFRJ')
        self.vis    = User.objects.create_user(    'visitante1',  'vis@bioflow.com',    'bio2026',  role='visitor',     first_name='Pedro',    last_name='Alves',    institution='PUC-Rio')
        self.stdout.write(self.style.SUCCESS('  7 usuarios criados'))

    def _criar_reagentes(self):
        dados = [
            ('Etanol absoluto',            'solvent',       'Sigma-Aldrich', 'SA-ETH-2024',  400,  500, 'mL', 'Sigma-Aldrich', 'Prateleira A1', '64-17-5'),
            ('Metanol grau HPLC',          'solvent',       'Tedia',         'TD-MET-2024',  300,  250, 'mL', 'Tedia Brasil',  'Prateleira A2', '67-56-1'),
            ('Acetonitrila grau HPLC',     'solvent',       'Tedia',         'TD-ACN-2024',  300,  200, 'mL', 'Tedia Brasil',  'Prateleira A3', '75-05-8'),
            ('Cloreto de Sodio',           'salt',          'Synth',         'SY-NACL-24',   730,  500, 'g',  'Synth',         'Prateleira B1', '7647-14-5'),
            ('Sulfato de Amonio',          'salt',          'Vetec',         'VT-SA-2024',   500,  200, 'g',  'Vetec',         'Prateleira B2', '7783-20-2'),
            ('Fosfato de Potassio',        'salt',          'Synth',         'SY-KPO-24',    500,   50, 'g',  'Synth',         'Prateleira B3', '7778-77-0'),
            ('Tampao PBS 10x',             'buffer',        'Gibco',         'GB-PBS-2024',   30, 1000, 'mL', 'Thermo Fisher', 'Geladeira 1',   ''),
            ('Tampao Tris-HCl pH 8',       'buffer',        'Sigma',         'SIG-TRS-24',   180,  500, 'mL', 'Sigma-Aldrich', 'Geladeira 1',   ''),
            ('Tampao acetato pH 5',        'buffer',        'Sigma',         'SIG-ACE-24',   180,  500, 'mL', 'Sigma-Aldrich', 'Geladeira 2',   ''),
            ('Lipase de Candida rugosa',   'enzyme',        'Sigma-Aldrich', 'SIG-LIP-88',   -10,   50, 'mg', 'Sigma-Aldrich', 'Freezer -20C',  '9001-62-1'),
            ('Lipase de Thermomyces',      'enzyme',        'Novozymes',     'NZ-LIP-2024',  365,   25, 'g',  'Novozymes',     'Freezer -20C',  ''),
            ('Protease Alcalase',          'enzyme',        'Novozymes',     'NZ-ALC-2024',  365,   20, 'g',  'Novozymes',     'Freezer -20C',  ''),
            ('Beta-Galactosidase',         'enzyme',        'Sigma',         'SIG-GAL-24',    25,   10, 'mg', 'Sigma-Aldrich', 'Freezer -80C',  '9031-11-2'),
            ('Glicose anidra',             'other',         'LabSynth',      'LS-GLU-2024',  730,  200, 'g',  'LabSynth',      'Prateleira C1', '50-99-7'),
            ('Peptona bacteriologica',     'culture_media', 'Acumedia',      'AC-PEP-2024',  730,  100, 'g',  'Acumedia',      'Prateleira C2', ''),
            ('Extrato de levedura',        'culture_media', 'Acumedia',      'AC-YE-2024',   730,  100, 'g',  'Acumedia',      'Prateleira C2', ''),
            ('Meio Czapek-Dox',            'culture_media', 'Himedia',       'HM-CZP-2024',  730,   50, 'g',  'Himedia',       'Prateleira C3', ''),
            ('Meio LB (Luria-Bertani)',     'culture_media', 'Sigma',         'SIG-LB-24',    730,  200, 'g',  'Sigma-Aldrich', 'Prateleira C3', ''),
            ('Agar bacteriologico',        'culture_media', 'LabSynth',      'LS-AGA-2024',  730,  100, 'g',  'LabSynth',      'Prateleira C4', ''),
            ('Azul de Coomassie R-250',    'dye',           'Bio-Rad',       'BR-COO-2024',  365,    5, 'g',  'Bio-Rad',       'Prateleira D1', '6104-59-2'),
            ('Reagente de Bradford',       'dye',           'Bio-Rad',       'BR-BRD-2024',   20,  100, 'mL', 'Bio-Rad',       'Geladeira 2',   ''),
            ('Lugol',                      'dye',           'Synth',         'SY-LUG-2024',  180,   50, 'mL', 'Synth',         'Prateleira D2', ''),
            ('Acido Cloridrico 37%',       'acid',          'Vetec',         'VT-HCL-2024',  730,  500, 'mL', 'Vetec',         'Armario acidos','7647-01-0'),
            ('Acido Acetico glacial',      'acid',          'Sigma',         'SIG-HAC-24',   730,  250, 'mL', 'Sigma-Aldrich', 'Armario acidos','64-19-7'),
            ('Hidroxido de Sodio',         'base',          'Synth',         'SY-NAO-2024',  730,  500, 'g',  'Synth',         'Prateleira B4', '1310-73-2'),
            ('Quitosana de baixo PM',      'other',         'Sigma',         'SIG-CHI-24',   730,   10, 'g',  'Sigma-Aldrich', 'Prateleira E1', '9012-76-4'),
            ('Alginato de sodio',          'other',         'Sigma',         'SIG-ALG-24',   730,   50, 'g',  'Sigma-Aldrich', 'Prateleira E1', '9005-38-3'),
            ('Oleo de oliva extra virgem', 'other',         'Importado',     'OLV-2024-01',  180,  500, 'mL', 'Mercado Local', 'Prateleira E2', ''),
            ('p-Nitrofenil palmitato',     'other',         'Sigma',         'SIG-NPP-24',   365,    1, 'g',  'Sigma-Aldrich', 'Freezer -20C',  '2364-21-0'),
            ('Sulfato de Magnesio',        'salt',          'Vetec',         'VT-MGS-2024',  500,    7, 'g',  'Vetec',         'Prateleira B5', '7487-88-9'),
        ]
        self.reagentes = []
        for nm, cat, mfr, lot, dias, qty, unit, sup, loc, cas in dados:
            exp = date.today() + timedelta(days=dias)
            r = Reagent.objects.create(
                name=nm, category=cat, manufacturer=mfr, lot=lot,
                expiration_date=exp, quantity=qty, unit=unit,
                supplier=sup, location=loc, cas_number=cas,
                created_by=self.admin
            )
            self.reagentes.append(r)
        self.stdout.write(self.style.SUCCESS(f'  {len(self.reagentes)} reagentes criados'))

    def _criar_equipamentos(self):
        dados = [
            ('HPLC Shimadzu',            'LC-20A',       'SHM-2019-001', 'Shimadzu',      'Lab Analitico',      'available',    90),
            ('Centrifuga Eppendorf',      '5430R',         'EP-2020-045',  'Eppendorf',     'Lab Microbiologia',  'available',    60),
            ('Biorreator BIOSTAT B',      'BIOSTAT B-DCU', 'BS-2021-012',  'Sartorius',     'Lab Fermentacao',    'in_use',      120),
            ('Espectrofotometro UV-Vis',  'Cary 60',       'AG-2022-007',  'Agilent',       'Lab Analitico',      'available',    45),
            ('NanoDrop 2000',             'NanoDrop 2000', 'TD-2022-003',  'Thermo Fisher', 'Lab Molecular',      'available',    90),
            ('Microscopio Olympus',       'BX53',          'OL-2020-033',  'Olympus',       'Lab Celular',        'maintenance',  30),
            ('Agitador Orbital 1',        'Innova S44i',   'NB-2021-088',  'New Brunswick', 'Lab Fermentacao',    'available',   180),
            ('Agitador Orbital 2',        'MaxQ 4000',     'TH-2022-015',  'Thermo Fisher', 'Lab Fermentacao',    'available',   180),
            ('Autoclave',                 'Vertical 75L',  'FAC-2019-002', 'Fabbe',         'Lab Suporte',        'available',    60),
            ('Banho-maria',               'SB-15',         'SB-2020-011',  'Solab',         'Lab Enzimologia',    'available',    90),
            ('Balanca analitica',         'AUY220',        'SHM-2021-006', 'Shimadzu',      'Lab Analitico',      'available',   120),
            ('Banho ultrassonico',        'USC-1450',      'USC-2020-004', 'Unique',        'Lab Enzimologia',    'available',    90),
            ('Estufa bacteriologica',     'SL-101',        'SL-2019-008',  'Solab',         'Lab Microbiologia',  'available',   180),
            ('pHmetro Mettler',           'FiveEasy F20',  'MT-2022-009',  'Mettler Toledo','Lab Analitico',      'available',   365),
            ('Liofilizador',              'L101',          'LZ-2021-001',  'Liotop',        'Lab Processamento',  'broken',        0),
            ('GC-MS Shimadzu',            'QP2020 NX',     'SHM-2023-001', 'Shimadzu',      'Lab Analitico',      'available',   180),
        ]
        self.equipamentos = []
        for nm, model, serial, mfr, loc, status, dias_manut in dados:
            manut = date.today() + timedelta(days=dias_manut) if dias_manut > 0 else None
            eq = Equipment.objects.create(
                name=nm, model=model, serial_number=serial,
                manufacturer=mfr, location=loc, status=status,
                maintenance_date=manut,
                acquisition_date=date.today() - timedelta(days=random.randint(300, 1500))
            )
            self.equipamentos.append(eq)

        EquipmentFailure.objects.create(equipment=self.equipamentos[5],  reported_by=self.tech1, description='Lampada do iluminador queimada. Substituicao solicitada ao fabricante.', resolved=False)
        EquipmentFailure.objects.create(equipment=self.equipamentos[14], reported_by=self.tech2, description='Bomba de vacuo com vazamento. Camara sem pressao adequada.',             resolved=False)
        EquipmentFailure.objects.create(equipment=self.equipamentos[1],  reported_by=self.tech1, description='Erro de calibracao no sensor de temperatura.',                           resolved=True)
        self.stdout.write(self.style.SUCCESS(f'  {len(self.equipamentos)} equipamentos criados (3 falhas registradas)'))

    def _criar_protocolos(self):
        dados = [
            ('Fermentacao Submersa de Lipase por Y. lipolytica',        'fermentation',   self.res1,  '3.0'),
            ('Fermentacao em Estado Solido - Substrato Agroindustrial',  'fermentation',   self.res2,  '1.2'),
            ('Extracao e Precipitacao de Lipase Extracelular',           'extraction',     self.res1,  '2.1'),
            ('Determinacao de Atividade Lipolitica (p-NPP)',             'enzymatic',      self.res1,  '4.0'),
            ('Determinacao de Proteina Total - Bradford',                'enzymatic',      self.admin, '2.0'),
            ('Imobilizacao em Alginato-Quitosana por Gelacao Ionica',   'enzymatic',      self.res3,  '1.5'),
            ('PCR para Confirmacao de Transformantes',                   'pcr',            self.res2,  '2.0'),
            ('Extracao de DNA Genomico - CTAB',                         'extraction',     self.res2,  '1.0'),
            ('Cromatografia de Troca Ionica em DEAE-Celulose',          'chromatography', self.res1,  '1.3'),
            ('Cromatografia de Afinidade - His-Tag Ni-NTA',             'chromatography', self.res3,  '1.0'),
            ('Microscopia de Fluorescencia - DAPI',                     'microscopy',     self.res3,  '1.0'),
            ('Sintese Enzimatica de Esteres em Sistema Livre de Solvente','enzymatic',    self.res1,  '2.0'),
        ]
        self.protocolos = []
        for titulo, cat, autor, versao in dados:
            p = Protocol.objects.create(
                title=titulo, category=cat,
                description=f'Protocolo padronizado para {titulo.lower()}. Desenvolvido e validado no laboratorio.',
                version=versao, author=autor, is_active=True
            )
            self.protocolos.append(p)
        self.stdout.write(self.style.SUCCESS(f'  {len(self.protocolos)} protocolos criados'))

    def _criar_amostras(self):
        dados = [
            ('Extrato bruto de lipase - Y. lipolytica IMUFRJ 50682', 'microbial',    self.res1,  -10, 'freezer_20', 'active'),
            ('Lipase imobilizada em alginato-quitosana (lote 1)',     'chemical',     self.res1,   -5, 'fridge_4',   'active'),
            ('Lipase imobilizada em alginato-quitosana (lote 2)',     'chemical',     self.res1,   -2, 'fridge_4',   'active'),
            ('Fracao proteica - pico cromatografico 1',               'chemical',     self.res1,   -7, 'freezer_80', 'active'),
            ('Fracao proteica - pico cromatografico 2',               'chemical',     self.res1,   -7, 'freezer_80', 'active'),
            ('Oleo de fritura usado (restaurante universitario)',      'chemical',     self.tech1,  -1, 'room_temp',  'active'),
            ('Biomassa seca Y. lipolytica - 48h fermentacao',         'microbial',    self.res1,  -14, 'freezer_20', 'active'),
            ('Sobrenadante pos-centrifugacao - fermentacao 72h',      'microbial',    self.res1,  -14, 'fridge_4',   'active'),
            ('Celulas competentes E. coli DH5a',                      'microbial',    self.res2,  -30, 'freezer_80', 'active'),
            ('Plasmideo pUB4-CRE purificado',                         'microbial',    self.res2,  -20, 'freezer_20', 'active'),
            ('Amostra de solo - Parque Nacional da Tijuca',           'environmental',self.res3,   -3, 'fridge_4',   'active'),
            ('Amostra de efluente industrial (pre-tratamento)',        'environmental',self.tech2,  -1, 'room_temp',  'active'),
            ('Produto de ester de fitosterol bruto',                  'chemical',     self.res1,   -8, 'room_temp',  'active'),
            ('Microparticulas de quitosana - spray drying',           'chemical',     self.res3,  -15, 'room_temp',  'active'),
            ('Preparado enzimatico comercial (controle positivo)',     'chemical',     self.admin, -60, 'fridge_4',   'active'),
            ('DNA genomico - Y. lipolytica',                          'microbial',    self.res2,  -25, 'freezer_20', 'active'),
            ('RNA total - celulas em fase exponencial',               'microbial',    self.res2,  -10, 'freezer_80', 'active'),
            ('Extrato proteico - fracao solavel 45% SA',              'chemical',     self.res1,  -20, 'freezer_20', 'consumed'),
            ('Amostra de biofilme - reator de leito fixo',            'microbial',    self.res3,   -5, 'fridge_4',   'active'),
            ('Produto hidrolisado enzimatico - oleo de peixe',        'chemical',     self.res1,  -12, 'fridge_4',   'active'),
        ]
        self.amostras = []
        for nm, tipo, resp, dias, armazen, status in dados:
            s = Sample.objects.create(
                name=nm, sample_type=tipo, responsible=resp,
                collection_date=date.today() + timedelta(days=dias),
                storage_location=armazen, status=status,
            )
            self.amostras.append(s)
        self.stdout.write(self.style.SUCCESS(f'  {len(self.amostras)} amostras criadas'))

    def _criar_experimentos(self):
        dados = [
            ('Producao de Lipase por Y. lipolytica em Erlenmeyers Alados',
             'Avaliacao do efeito de diferentes geometrias de Erlenmeyer sobre a transferencia de oxigenio e producao de lipase extracelular.',
             self.res1, 0, 'in_progress', -14, [0,3,13,14,16,17,28], [0,5,6,7]),
            ('Sintese Enzimatica de Beta-Sitosterol Oleato por Lipase CRL',
             'Sintese de ester de fitosterol utilizando lipase de Candida rugosa em sistema livre de solvente.',
             self.res1, 11, 'in_progress', -7, [9,27,28], [1,2,12]),
            ('Encapsulacao de Lipase em Microcapsulas de Alginato-Quitosana',
             'Imobilizacao de lipase por gelacao ionica em microparticulas de alginato revestidas com quitosana.',
             self.res1, 5, 'completed', -45, [9,25,26,7], [1,2]),
            ('Expressao Heterologa de Lipase em E. coli BL21',
             'Clonagem do gene LIP2 de Y. lipolytica no vetor pET-28a e expressao em E. coli BL21(DE3).',
             self.res2, 9, 'in_progress', -21, [0,4,24,3], [8,9,15,16]),
            ('Producao de Beta-Galactosidase por Aspergillus niger',
             'Fermentacao submersa para producao de beta-galactosidase com avaliacao de diferentes fontes de carbono.',
             self.res2, 0, 'planning', 3, [13,14,15,18], [10]),
            ('Biorremediacao de Efluente Lipidico por Lipase Imobilizada',
             'Avaliacao da eficiencia de hidrolise de efluente industrial rico em gordura por lipase imobilizada em alginato.',
             self.res3, 3, 'in_progress', -10, [9,25,26,28], [11,1]),
            ('Sintese de Biodiesel Enzimatico a partir de Oleo de Fritura',
             'Transesterificacao enzimatica de oleo de fritura usando lipase de Thermomyces lanuginosus imobilizada.',
             self.tech1, 11, 'paused', -30, [10,0,1,27], [5,12]),
            ('Caracterizacao Molecular de Microrganismos Produtores de Lipase',
             'Isolamento de microrganismos produtores de lipase de amostras ambientais e identificacao por 16S rRNA.',
             self.res3, 7, 'in_progress', -18, [15,16,4,3], [10,11]),
            ('Otimizacao da Imobilizacao de Lipase por Spray Drying',
             'Comparacao de agentes encapsulantes para imobilizacao de lipase por spray drying.',
             self.res3, 5, 'planning', 7, [25,26,9], [13,14]),
            ('Producao de DAG e MAG por Hidrolise Parcial de Triglicerideos',
             'Hidrolise enzimatica controlada de triglicerideos de oleo de peixe por lipase 1,3-especifica.',
             self.res1, 3, 'completed', -60, [9,10,28], [19,5]),
        ]
        self.experimentos = []
        for titulo, desc, resp, prot_idx, status, dias, reag_idx, amos_idx in dados:
            e = Experiment.objects.create(
                title=titulo, description=desc, responsible=resp,
                protocol=self.protocolos[prot_idx], status=status,
                start_date=date.today() + timedelta(days=dias),
                end_date=date.today() + timedelta(days=dias+60) if status != 'completed' else None,
                actual_end_date=date.today() + timedelta(days=dias+45) if status == 'completed' else None,
            )
            e.reagents.set([self.reagentes[i] for i in reag_idx])
            e.samples.set([self.amostras[i] for i in amos_idx])
            e.participants.set(random.sample(
                [self.admin, self.res1, self.res2, self.res3, self.tech1, self.tech2],
                k=random.randint(1, 3)
            ))
            self.experimentos.append(e)
        self.stdout.write(self.style.SUCCESS(f'  {len(self.experimentos)} experimentos criados'))

    def _criar_analises(self):
        dados = [
            (0, self.res1,  'enzymatic_activity', 'Atividade lipolitica - 24h de fermentacao',     8.3,  'U/mL', 0,  -13),
            (0, self.res1,  'enzymatic_activity', 'Atividade lipolitica - 48h de fermentacao',    15.7,  'U/mL', 0,  -11),
            (0, self.res1,  'enzymatic_activity', 'Atividade lipolitica - 72h de fermentacao',    22.4,  'U/mL', 0,   -9),
            (0, self.res1,  'enzymatic_activity', 'Atividade lipolitica - 96h de fermentacao',    18.1,  'U/mL', 0,   -7),
            (0, self.res1,  'microbial_growth',   'Biomassa seca - 24h',                           2.1,  'g/L',  6,  -13),
            (0, self.res1,  'microbial_growth',   'Biomassa seca - 48h',                           5.8,  'g/L',  6,  -11),
            (0, self.res1,  'microbial_growth',   'Biomassa seca - 72h',                           8.9,  'g/L',  6,   -9),
            (0, self.admin, 'concentration',      'Proteina total Bradford - extrato 72h',          1.82,'mg/mL', 3,   -7),
            (1, self.res1,  'enzymatic_activity', 'Atividade lipolitica - lipase livre 40C',       42.5, 'U/mg', 3,   -6),
            (1, self.res1,  'enzymatic_activity', 'Atividade lipolitica - lipase imob. 40C',       35.8, 'U/mg', 3,   -5),
            (1, self.res1,  'enzymatic_activity', 'Atividade lipolitica - lipase imob. 50C',       31.2, 'U/mg', 3,   -4),
            (1, self.res1,  'chromatogram',       'Cromatograma HPLC - produto de sintese 24h',    None, '',     0,   -3),
            (2, self.res1,  'enzymatic_activity', 'Eficiencia de encapsulacao - lote 1',           87.3, '%',    3,  -40),
            (2, self.res1,  'enzymatic_activity', 'Atividade recuperada pos-imobilizacao',         65.1, '%',    3,  -35),
            (2, self.res1,  'concentration',      'Proteina total sobrenadante pos-encapsulacao',   0.23,'mg/mL', 3, -38),
            (3, self.res2,  'concentration',      'Proteina His-Tag purificada - eluato Ni-NTA',    0.95,'mg/mL', 3, -15),
            (3, self.res2,  'enzymatic_activity', 'Atividade da lipase recombinante His-Tag',      18.4, 'U/mg', 3,  -14),
            (5, self.res3,  'enzymatic_activity', 'Atividade residual lipase - efluente 2h',       92.3, '%',    3,   -8),
            (5, self.res3,  'enzymatic_activity', 'Atividade residual lipase - efluente 6h',       74.5, '%',    3,   -6),
            (5, self.res3,  'concentration',      'Acidos graxos livres - hidrolise 6h',          345.2, 'mg/L', 3,   -5),
            (6, self.tech1, 'chromatogram',       'Cromatograma GC - esteres metilicos (FAME)',    None, '',    15,  -25),
            (6, self.tech1, 'concentration',      'Rendimento em esteres metilicos - 24h',         72.1, '%',   15,  -24),
            (6, self.tech1, 'concentration',      'Rendimento em esteres metilicos - 48h',         85.4, '%',   15,  -22),
            (7, self.res3,  'other',              'Sequenciamento 16S rRNA - isolado BFL-01',       None,'',     4,  -15),
            (7, self.res3,  'enzymatic_activity', 'Atividade lipolitica - isolado BFL-01',          5.6, 'U/mL', 3, -12),
            (7, self.res3,  'enzymatic_activity', 'Atividade lipolitica - isolado BFL-03',          9.1, 'U/mL', 3, -10),
            (9, self.res1,  'chromatogram',       'Cromatograma HPLC - DAG e MAG produto final',   None, '',    0,  -55),
            (9, self.res1,  'concentration',      'Rendimento DAG - hidrolise parcial 4h',          38.7,'%',    3,  -52),
            (9, self.res1,  'concentration',      'Rendimento MAG - hidrolise parcial 4h',          12.3,'%',    3,  -52),
        ]
        for exp_idx, analista, tipo, nome, resultado, unidade, eq_idx, dias in dados:
            Analysis.objects.create(
                experiment=self.experimentos[exp_idx],
                analyst=analista, analysis_type=tipo, name=nome,
                numeric_result=resultado, result_unit=unidade,
                equipment_used=self.equipamentos[eq_idx] if resultado is not None else None,
                analysis_date=date.today() + timedelta(days=dias),
                observations='Analise realizada conforme protocolo padrao do laboratorio.'
            )
        self.stdout.write(self.style.SUCCESS(f'  {len(dados)} analises criadas'))

    def _criar_agendamentos(self):
        agendamentos = [
            (0,  self.res1,   0,  9,  12, 'Analise cromatografica de amostras lipidicas',     'confirmed'),
            (1,  self.tech1,  0, 14,  16, 'Centrifugacao pos-fermentacao Y. lipolytica 72h',  'confirmed'),
            (2,  self.res1,   0, 10,  14, 'Controle de agitacao e aeracao - biorreator',      'confirmed'),
            (3,  self.res2,   0,  9,  11, 'Leitura de absorbancia - curva de crescimento',    'confirmed'),
            (15, self.res1,   0, 14,  17, 'Quantificacao GC-MS - esteres metilicos',          'confirmed'),
            (10, self.admin,  0,  8,  10, 'Pesagem e calibracao de balanca analitica',        'confirmed'),
            (8,  self.tech2,  0,  9,  12, 'Esterilizacao de meio de cultura 121C/20min',      'confirmed'),
            (0,  self.res3,   0, 13,  16, 'HPLC - caracterizacao de isolados ambientais',     'confirmed'),
            (0,  self.res1,  -1,  9,  12, 'Analise cromatografica - sintese ester dia 1',     'completed'),
            (15, self.res2,  -2,  9,  12, 'GC-MS - confirmacao estrutural FAME',              'completed'),
            (1,  self.tech1, -3, 14,  16, 'Preparo de meio e inoculacao DAG',                 'completed'),
            (0,  self.res1,   1,  9,  12, 'Analise cromatografica - produto sintese dia 2',   'confirmed'),
            (3,  self.res2,   2,  8,  10, 'Extracao de DNA - amostras ambientais para PCR',   'confirmed'),
        ]
        count = 0
        for eq_idx, user, dia_delta, hora_i, hora_f, purpose, status in agendamentos:
            start = timezone.now().replace(hour=hora_i, minute=0, second=0, microsecond=0) + timedelta(days=dia_delta)
            end   = timezone.now().replace(hour=hora_f, minute=0, second=0, microsecond=0) + timedelta(days=dia_delta)
            try:
                Schedule.objects.create(
                    equipment=self.equipamentos[eq_idx], user=user,
                    start_datetime=start, end_datetime=end,
                    purpose=purpose, status=status
                )
                count += 1
            except Exception:
                pass
        self.stdout.write(self.style.SUCCESS(f'  {count} agendamentos criados'))

    def _criar_movimentacoes(self):
        dados = [
            (9,  'exit',       10, 'Uso no experimento de sintese de ester',              self.experimentos[1]),
            (27, 'exit',       50, 'Uso no experimento de sintese de ester',              self.experimentos[1]),
            (0,  'exit',      100, 'Solvente de lavagem - purificacao cromatografica',    self.experimentos[3]),
            (6,  'exit',      200, 'Preparo de tampao PBS 1x para lavagem de celulas',    self.experimentos[3]),
            (13, 'exit',       20, 'Preparo de curva padrao Bradford',                    None),
            (3,  'entry',     200, 'Recebimento novo lote - NF-2024-0891',                None),
            (14, 'entry',     100, 'Reposicao de estoque - pedido aprovado',              None),
            (15, 'entry',      50, 'Reposicao de estoque - pedido aprovado',              None),
            (25, 'exit',        5, 'Preparo de microparticulas de quitosana lote 3',      self.experimentos[1]),
            (26, 'exit',       10, 'Preparo de microesferas - encapsulacao',              self.experimentos[2]),
            (20, 'exit',       20, 'Determinacao de proteina total - Bradford serie 1',   None),
            (10, 'exit',        5, 'Reacao de transesterificacao enzimatica',             self.experimentos[6]),
            (28, 'exit',      100, 'Substrato para ensaio de atividade p-NPP',            None),
            (4,  'exit',       20, 'Precipitacao de proteinas - ensaio 1',               self.experimentos[0]),
            (0,  'adjustment', 50, 'Ajuste de inventario - auditoria mensal',             None),
        ]
        for reag_idx, tipo, qty, motivo, exp in dados:
            r = self.reagentes[reag_idx]
            prev = r.quantity
            new_q = prev + qty if tipo in ('entry', 'adjustment') else max(prev - qty, 0)
            InventoryMovement.objects.create(
                reagent=r, movement_type=tipo, quantity=qty,
                previous_quantity=prev, new_quantity=new_q,
                reason=motivo, experiment=exp,
                performed_by=random.choice([self.admin, self.tech1, self.tech2])
            )
            r.quantity = new_q
            r.save()
        self.stdout.write(self.style.SUCCESS(f'  {len(dados)} movimentacoes criadas'))

    def _resumo(self):
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('  BioFlow - banco populado com sucesso!'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(f'  Usuarios:      {User.objects.count()}')
        self.stdout.write(f'  Reagentes:     {Reagent.objects.count()}')
        self.stdout.write(f'  Equipamentos:  {Equipment.objects.count()}')
        self.stdout.write(f'  Protocolos:    {Protocol.objects.count()}')
        self.stdout.write(f'  Amostras:      {Sample.objects.count()}')
        self.stdout.write(f'  Experimentos:  {Experiment.objects.count()}')
        self.stdout.write(f'  Analises:      {Analysis.objects.count()}')
        self.stdout.write(f'  Agendamentos:  {Schedule.objects.count()}')
        self.stdout.write(f'  Movimentacoes: {InventoryMovement.objects.count()}')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write('  Admin:   admin / admin123')
        self.stdout.write('  Pesq.:   ana.costa / bio2026')
        self.stdout.write('  Tecnico: tecnico1 / bio2026')
        self.stdout.write(self.style.SUCCESS('=' * 50))
