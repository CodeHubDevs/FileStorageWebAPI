# Generated by Django 4.1.7 on 2023-03-20 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('files', '0001_initial'),
        ('modules', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='filemodel',
            name='module_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modules.modulemodel'),
        ),
    ]
