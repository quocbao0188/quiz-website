# Generated by Django 3.0.3 on 2020-04-08 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docum', '0005_auto_20200408_0830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.AddField(
            model_name='document',
            name='species',
            field=models.CharField(choices=[('DOC', 'Document'), ('LAB', 'Practice lab'), ('OTH', 'Other')], default='DOC', max_length=3, verbose_name='Species'),
        ),
        migrations.AddField(
            model_name='order',
            name='doc_items',
            field=models.ManyToManyField(blank=True, to='docum.Document', verbose_name='Document items'),
        ),
        migrations.AlterField(
            model_name='document',
            name='link_url',
            field=models.URLField(max_length=255, unique=True, verbose_name='Direct link'),
        ),
    ]