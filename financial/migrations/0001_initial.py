# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FiAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100, choices=[(b'E', b'Expense'), (b'R', b'Revenue')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FiAccountGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FiBank',
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
            name='FiCostCenter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.ForeignKey(to='financial.FiAccount')),
                ('account_group', models.ForeignKey(to='financial.FiAccountGroup')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FiCurrentAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('agency', models.PositiveIntegerField()),
                ('number', models.PositiveIntegerField()),
                ('bank', models.ForeignKey(to='financial.FiBank')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FiDocumentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FiEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('document_number', models.CharField(max_length=100)),
                ('cheque_number', models.CharField(max_length=100, null=True, blank=True)),
                ('expiration_date', models.DateField()),
                ('record', models.CharField(max_length=255, null=True, blank=True)),
                ('value', models.DecimalField(max_digits=10, decimal_places=2)),
                ('category', models.CharField(max_length=1, choices=[(b'1', b'ONE'), (b'2', b'TWO')])),
                ('status', models.CharField(max_length=2, choices=[(b'R', b'Receivable'), (b'P', b'Payable'), (b'RR', b'Received'), (b'PP', b'Paid')])),
                ('client_supplier', models.ForeignKey(to='main.MaCustomerSupplier')),
                ('costcenter', models.ForeignKey(to='financial.FiCostCenter')),
                ('current_account', models.ForeignKey(to='financial.FiCurrentAccount')),
                ('department', models.ForeignKey(to='main.MaDepartment')),
                ('document_type', models.ForeignKey(to='financial.FiDocumentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FiSubaccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FiSubaccountType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('nature', models.CharField(max_length=2, choices=[(b'O', b'Operational'), (b'OO', b'One-off'), (b'I', b'Indirect')])),
                ('subaccount', models.ForeignKey(to='financial.FiSubaccount')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FiWriteOff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('value', models.DecimalField(max_digits=10, decimal_places=2)),
                ('third_party', models.CharField(max_length=100, null=True, blank=True)),
                ('third_party_agency', models.CharField(max_length=30, null=True, blank=True)),
                ('third_party_bank', models.ForeignKey(blank=True, to='financial.FiBank', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='fientry',
            name='write_off',
            field=models.OneToOneField(to='financial.FiWriteOff'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='ficurrentaccount',
            unique_together=set([('bank', 'agency', 'number')]),
        ),
        migrations.AddField(
            model_name='ficostcenter',
            name='subaccount',
            field=models.ForeignKey(to='financial.FiSubaccount'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ficostcenter',
            name='subaccount_type',
            field=models.ForeignKey(to='financial.FiSubaccountType'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='ficostcenter',
            unique_together=set([('account_group', 'account', 'subaccount', 'subaccount_type')]),
        ),
    ]
