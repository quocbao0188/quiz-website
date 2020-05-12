# Generated by Django 3.0.5 on 2020-05-11 08:33

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, verbose_name='Clean URL')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, verbose_name='Clean URL')),
                ('species', models.CharField(choices=[('DOC', 'Document'), ('LAB', 'Practice lab'), ('OTH', 'Other')], default='DOC', max_length=3, verbose_name='Species')),
                ('content', models.TextField(verbose_name='Description')),
                ('link_url', models.URLField(max_length=255, unique=True, verbose_name='Direct link')),
                ('image', models.ImageField(default='hushare-default.png', null=True, upload_to='')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Created')),
                ('credit', models.DecimalField(decimal_places=0, default=Decimal('0'), max_digits=8)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('catago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='docum.Category', verbose_name='Category')),
                ('like', models.ManyToManyField(blank=True, related_name='docs_likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docum.Document', verbose_name='Items')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(verbose_name='Comment content')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='docum.Document')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
