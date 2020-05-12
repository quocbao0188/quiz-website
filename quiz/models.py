from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from PIL import Image
from django.utils import timezone

class CategoryQuiz(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, verbose_name = "Clean URL")

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) # set the slug explicitly
        super(CategoryQuiz, self).save(*args, **kwargs) # call Django's save()

class Quiz(models.Model):
    title = models.CharField(max_length=1000)
    slug = models.SlugField(unique=True, verbose_name="Clean URL")
    publish = models.BooleanField(blank=True, default=False, verbose_name="Publish",help_text="If yes, the quiz is displayed in the quiz list")
    category_quiz = models.ForeignKey(CategoryQuiz, on_delete=models.CASCADE, verbose_name='Category', related_name='quizs')
    description = models.TextField(verbose_name = "Description")
    time = models.PositiveSmallIntegerField(verbose_name='Timer for quiz', help_text='Planning your time for a quiz. Minute units', default=10)
    image = models.ImageField(default='hushare-default.png', null=True)
    create_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.title

    # Ghi đè hàm save() đẻ chỉnh kích thước ảnh xuống 300px x 200px
    def save(self, **kwargs):
        # Ghi đè phương thức save()
        super().save()
        img = Image.open(self.image.path)
        if img.height > 750 or img.width > 450:
            output_size = (750, 450)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    label = models.TextField()

    def __str__(self):
        return self.label

    # def get_answers_list(self):
    #     return [(answer.id, answer.text) for answer in Answer.objects.filter(question=self)]



class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=1000)
    is_correct = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.text

    

class Transcript(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_item = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name = "Quiz items")
    total_score = models.FloatField(default=0, verbose_name = "Total score")
    answer_correct = models.PositiveSmallIntegerField(default=0, verbose_name='Total number of correct answers')
    question_number = models.PositiveSmallIntegerField(default=0, verbose_name='Total questions')
    create_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f'{self.user.username} {self.quiz_item.title} test score'

@receiver(pre_save, sender=Quiz)
def slugify_title(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title)
