# Generated by Django 2.1.7 on 2019-02-26 07:46

from django.db import migrations, models
import django.db.models.deletion
import mreg.validators


class Migration(migrations.Migration):

    dependencies = [
        ('mreg', '0004_auto_20190222_1338'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mx',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.PositiveIntegerField(validators=[mreg.validators.validate_16bit_uint])),
                ('mx', models.TextField(max_length=253, validators=[mreg.validators.validate_hostname])),
                ('host', models.ForeignKey(db_column='host', on_delete=django.db.models.deletion.CASCADE, related_name='mxs', to='mreg.Host')),
            ],
            options={
                'db_table': 'mx',
            },
        ),
        migrations.AlterUniqueTogether(
            name='mx',
            unique_together={('host', 'priority', 'mx')},
        ),
    ]