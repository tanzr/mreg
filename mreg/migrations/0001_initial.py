# Generated by Django 2.1.3 on 2018-11-30 08:31

from django.db import migrations, models
import django.db.models.deletion
import mreg.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cname',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.TextField()),
                ('ttl', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'cname',
            },
        ),
        migrations.CreateModel(
            name='HinfoPreset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu', models.TextField()),
                ('os', models.TextField()),
            ],
            options={
                'db_table': 'hinfo_preset',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=253, unique=True, validators=[mreg.validators.validate_hostname])),
                ('contact', models.EmailField(max_length=254)),
                ('ttl', models.IntegerField(blank=True, null=True)),
                ('loc', models.TextField(blank=True, null=True, validators=[mreg.validators.validate_loc])),
                ('comment', models.TextField(blank=True, null=True)),
                ('hinfo', models.ForeignKey(blank=True, db_column='hinfo', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mreg.HinfoPreset')),
            ],
            options={
                'db_table': 'host',
            },
        ),
        migrations.CreateModel(
            name='Ipaddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipaddress', models.GenericIPAddressField()),
                ('macaddress', models.TextField(blank=True, null=True, validators=[mreg.validators.validate_mac_address])),
                ('host', models.ForeignKey(db_column='host', on_delete=django.db.models.deletion.CASCADE, related_name='ipaddresses', to='mreg.Host')),
            ],
            options={
                'db_table': 'ipaddress',
            },
        ),
        migrations.CreateModel(
            name='ModelChangeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(max_length=132)),
                ('table_row', models.BigIntegerField()),
                ('data', models.TextField()),
                ('action', models.CharField(max_length=16)),
                ('timestamp', models.DateTimeField()),
            ],
            options={
                'db_table': 'model_change_log',
            },
        ),
        migrations.CreateModel(
            name='NameServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=253, unique=True, validators=[mreg.validators.validate_hostname])),
                ('ttl', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ns',
            },
        ),
        migrations.CreateModel(
            name='Naptr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference', models.IntegerField(blank=True, null=True)),
                ('orderv', models.IntegerField(blank=True, null=True)),
                ('flag', models.CharField(blank=True, max_length=1, null=True, validators=[mreg.validators.validate_naptr_flag])),
                ('service', models.TextField()),
                ('regex', models.TextField(blank=True, null=True)),
                ('replacement', models.TextField()),
                ('host', models.ForeignKey(db_column='host', on_delete=django.db.models.deletion.CASCADE, related_name='naptrs', to='mreg.Host')),
            ],
            options={
                'db_table': 'naptr',
            },
        ),
        migrations.CreateModel(
            name='PtrOverride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipaddress', models.GenericIPAddressField(unique=True)),
                ('host', models.ForeignKey(db_column='host', on_delete=django.db.models.deletion.CASCADE, related_name='ptr_overrides', to='mreg.Host')),
            ],
            options={
                'db_table': 'ptr_override',
            },
        ),
        migrations.CreateModel(
            name='Srv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.TextField(validators=[mreg.validators.validate_srv_service_text])),
                ('priority', models.IntegerField(blank=True, null=True)),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('port', models.IntegerField(blank=True, null=True)),
                ('ttl', models.IntegerField(blank=True, null=True)),
                ('target', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'srv',
            },
        ),
        migrations.CreateModel(
            name='Subnet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('range', models.TextField(unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('vlan', models.IntegerField(blank=True, null=True)),
                ('dns_delegated', models.NullBooleanField()),
                ('category', models.TextField(blank=True, null=True)),
                ('location', models.TextField(blank=True, null=True)),
                ('frozen', models.NullBooleanField()),
                ('reserved', models.PositiveIntegerField(default=3)),
            ],
            options={
                'db_table': 'subnet',
                'ordering': ('range',),
            },
        ),
        migrations.CreateModel(
            name='Txt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txt', models.TextField(max_length=255)),
                ('host', models.ForeignKey(db_column='host', on_delete=django.db.models.deletion.CASCADE, related_name='txts', to='mreg.Host')),
            ],
            options={
                'db_table': 'txt',
            },
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=253, unique=True, validators=[mreg.validators.validate_zonename])),
                ('primary_ns', models.CharField(max_length=253, validators=[mreg.validators.validate_hostname])),
                ('email', models.EmailField(max_length=254)),
                ('serialno', models.BigIntegerField(blank=True, null=True, validators=[mreg.validators.validate_zones_serialno])),
                ('refresh', models.IntegerField(default=10800)),
                ('retry', models.IntegerField(default=3600)),
                ('expire', models.IntegerField(default=1814400)),
                ('ttl', models.IntegerField(default=43200)),
                ('nameservers', models.ManyToManyField(db_column='ns', to='mreg.NameServer')),
            ],
            options={
                'db_table': 'zone',
            },
        ),
        migrations.AddField(
            model_name='txt',
            name='zone',
            field=models.ForeignKey(blank=True, db_column='zone', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mreg.Zone'),
        ),
        migrations.AddField(
            model_name='srv',
            name='zone',
            field=models.ForeignKey(blank=True, db_column='zone', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mreg.Zone'),
        ),
        migrations.AddField(
            model_name='naptr',
            name='zone',
            field=models.ForeignKey(blank=True, db_column='zone', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mreg.Zone'),
        ),
        migrations.AddField(
            model_name='host',
            name='zone',
            field=models.ForeignKey(blank=True, db_column='zone', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mreg.Zone'),
        ),
        migrations.AlterUniqueTogether(
            name='hinfopreset',
            unique_together={('cpu', 'os')},
        ),
        migrations.AddField(
            model_name='cname',
            name='host',
            field=models.ForeignKey(db_column='host', on_delete=django.db.models.deletion.CASCADE, related_name='cnames', to='mreg.Host'),
        ),
        migrations.AddField(
            model_name='cname',
            name='zone',
            field=models.ForeignKey(blank=True, db_column='zone', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mreg.Zone'),
        ),
        migrations.AlterUniqueTogether(
            name='ipaddress',
            unique_together={('host', 'ipaddress')},
        ),
    ]
