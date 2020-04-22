# Generated by Django 3.0.4 on 2020-04-21 08:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000)),
                ('is_correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, verbose_name='Clean URL')),
            ],
        ),
        migrations.CreateModel(
            name='QuizProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_score', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('slug', models.SlugField(help_text='A URL slug is the part of a URL or link that comes after the domain extension', unique=True, verbose_name='Clean URL')),
                ('description', models.CharField(max_length=70)),
                ('time', models.PositiveSmallIntegerField(default=10, help_text='Planning your time for a quiz', verbose_name='Time for quiz')),
                ('image', models.ImageField(null=True, upload_to='')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('category_quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.CategoryQuiz', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Quiz',
                'verbose_name_plural': 'Quizzes',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=1000)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='AttemptedQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_correct', models.BooleanField(default=False)),
                ('marks_obtained', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Question')),
                ('quiz_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='quiz.QuizProfile')),
                ('selected_answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Answer')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='quiz.Question'),
        ),
    ]
