# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MaBank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MaBankAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveIntegerField()),
                ('bank', models.ForeignKey(to='main.MaBank')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MaCustomerSupplier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('fantasy_name', models.CharField(max_length=255)),
                ('contact_name', models.CharField(max_length=255)),
                ('person_type', models.CharField(max_length=10, choices=[(b'N', b'Natural'), (b'L', b'Legal')])),
                ('cpf', models.CharField(max_length=14)),
                ('rg', models.CharField(max_length=14)),
                ('cnpj', models.CharField(max_length=18)),
                ('state_registration', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('site', models.URLField(null=True, blank=True)),
                ('phone1', models.CharField(max_length=20, null=True, blank=True)),
                ('phone2', models.CharField(max_length=20, null=True, blank=True)),
                ('address', models.CharField(max_length=255, null=True, blank=True)),
                ('address_number', models.CharField(max_length=15, null=True, blank=True)),
                ('address_complement', models.CharField(max_length=255, null=True, blank=True)),
                ('city', models.CharField(max_length=255, null=True, blank=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amap\xe1'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Cear\xe1'), ('DF', 'Distrito Federal'), ('ES', 'Esp\xedrito Santo'), ('GO', 'Goi\xe1s'), ('MA', 'Maranh\xe3o'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Par\xe1'), ('PB', 'Para\xedba'), ('PR', 'Paran\xe1'), ('PE', 'Pernambuco'), ('PI', 'Piau\xed'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rond\xf4nia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'S\xe3o Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')])),
                ('zipcode', models.CharField(max_length=255, null=True, blank=True)),
                ('neighborhood', models.CharField(max_length=255, null=True, blank=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(max_length=10, choices=[(b'C', b'Customer'), (b'S', b'Supplier'), (b'C/S', b'Customer and Supplier')])),
                ('bank_accounts', models.ManyToManyField(to='main.MaBankAccount')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MaDepartment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MaEmployee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('fantasy_name', models.CharField(max_length=255)),
                ('contact_name', models.CharField(max_length=255)),
                ('person_type', models.CharField(max_length=10, choices=[(b'N', b'Natural'), (b'L', b'Legal')])),
                ('cpf', models.CharField(max_length=14)),
                ('rg', models.CharField(max_length=14)),
                ('cnpj', models.CharField(max_length=18)),
                ('state_registration', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('site', models.URLField(null=True, blank=True)),
                ('phone1', models.CharField(max_length=20, null=True, blank=True)),
                ('phone2', models.CharField(max_length=20, null=True, blank=True)),
                ('address', models.CharField(max_length=255, null=True, blank=True)),
                ('address_number', models.CharField(max_length=15, null=True, blank=True)),
                ('address_complement', models.CharField(max_length=255, null=True, blank=True)),
                ('city', models.CharField(max_length=255, null=True, blank=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amap\xe1'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Cear\xe1'), ('DF', 'Distrito Federal'), ('ES', 'Esp\xedrito Santo'), ('GO', 'Goi\xe1s'), ('MA', 'Maranh\xe3o'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Par\xe1'), ('PB', 'Para\xedba'), ('PR', 'Paran\xe1'), ('PE', 'Pernambuco'), ('PI', 'Piau\xed'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rond\xf4nia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'S\xe3o Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')])),
                ('zipcode', models.CharField(max_length=255, null=True, blank=True)),
                ('neighborhood', models.CharField(max_length=255, null=True, blank=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(to='main.MaDepartment')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MaEmployeeFunction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MaEquipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=100, null=True, blank=True)),
                ('model', models.CharField(max_length=100, null=True, blank=True)),
                ('registration', models.CharField(max_length=100, null=True, blank=True)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MaEquipmentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='maequipment',
            name='equipment_type',
            field=models.ForeignKey(to='main.MaEquipmentType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='maemployee',
            name='function',
            field=models.ForeignKey(to='main.MaEmployeeFunction'),
            preserve_default=True,
        ),
    ]
