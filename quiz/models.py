from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from PIL import Image

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
    slug = models.SlugField(unique=True, verbose_name="Clean URL", help_text='A URL slug is the part of a URL or link that comes after the domain extension')
    category_quiz = models.ForeignKey(CategoryQuiz, on_delete=models.CASCADE, verbose_name='Category', related_name='quizs')
    description = models.CharField(max_length=70)
    time = models.PositiveSmallIntegerField(verbose_name='Time for quiz', help_text='Planning your time for a quiz', default=10)
    image = models.ImageField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

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
    label = models.CharField(max_length=1000)

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

    



class QuizProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_score = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    def __str__(self):
        return self.user.username


class AttemptedQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz_profile = models.ForeignKey(QuizProfile, on_delete=models.CASCADE, related_name='attempts')
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    is_correct = models.BooleanField(default=False, null=False)
    marks_obtained = models.DecimalField(default=0, decimal_places=2, max_digits=6)


@receiver(pre_save, sender=Quiz)
def slugify_title(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title)
