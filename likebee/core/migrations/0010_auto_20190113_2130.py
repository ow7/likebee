# Generated by Django 2.1.5 on 2019-01-13 23:30

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20190113_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='level',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='lft',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core.Task'),
        ),
        migrations.AddField(
            model_name='task',
            name='rght',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
    ]