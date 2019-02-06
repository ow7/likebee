# Generated by Django 2.1.5 on 2019-02-06 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_task_task_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['status', 'priority'], 'verbose_name': 'Tarefa', 'verbose_name_plural': 'Tarefas'},
        ),
        migrations.AddField(
            model_name='status',
            name='archive',
            field=models.BooleanField(default=False, verbose_name='Arquivado?'),
        ),
    ]
