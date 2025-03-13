# Generated by Django 5.1.6 on 2025-03-12 23:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('times', '0019_equipo_jugador_liga_mlbteam_contrato_ligateams_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('tipo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TrxTyp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=200)),
                ('codigo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Trx',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('monto', models.DecimalField(decimal_places=2, default=0.0, max_digits=16)),
                ('desc', models.CharField(max_length=200)),
                ('debito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='times.cuenta')),
                ('credito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='times.trxtyp')),
            ],
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anho', models.IntegerField()),
                ('mes', models.IntegerField()),
                ('mbudget', models.DecimalField(decimal_places=2, default=0.0, max_digits=16)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='times.trxtyp')),
            ],
        ),
    ]
