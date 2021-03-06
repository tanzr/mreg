# Generated by Django 2.1.5 on 2019-02-01 09:56

from django.db import migrations, models
import django.db.models.deletion
import mreg.models
import mreg.validators


class Migration(migrations.Migration):

    dependencies = [
        ('mreg', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForwardZoneDelegation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=253, unique=True, validators=[mreg.validators.validate_hostname])),
                ('nameservers', models.ManyToManyField(db_column='ns', to='mreg.NameServer')),
                ('zone', models.ForeignKey(db_column='zone', on_delete=django.db.models.deletion.CASCADE, related_name='delegations', to='mreg.ForwardZone')),
            ],
            options={
                'db_table': 'forward_zone_delegation',
            },
            bases=(models.Model, mreg.models.ZoneHelpers),
        ),
        migrations.CreateModel(
            name='ReverseZoneDelegation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=253, unique=True, validators=[mreg.validators.validate_reverse_zone_name])),
                ('nameservers', models.ManyToManyField(db_column='ns', to='mreg.NameServer')),
                ('zone', models.ForeignKey(db_column='zone', on_delete=django.db.models.deletion.CASCADE, related_name='delegations', to='mreg.ReverseZone')),
            ],
            options={
                'db_table': 'reverse_zone_delegation',
            },
            bases=(models.Model, mreg.models.ZoneHelpers),
        ),
    ]
