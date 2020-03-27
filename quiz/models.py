from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.utils.text import slugify
#from django.db.models.signals import pre_save
# Create your models here.

class Post(models.Model):
    genre = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) # set the slug explicitly
        super(Post, self).save(*args, **kwargs) # call Django's save()

    def get_absolute_url(self):
        return reverse("quiz-detail", kwargs={"slug": self.slug})

    def get_like_url(self):
        return reverse("quiz-like", kwargs={"slug": self.slug})

    def get_api_like_url(self):
        return reverse("quiz-api-like", kwargs={"slug": self.slug})

    # Ghi đè hàm save() đẻ chỉnh kích thước ảnh xuống 300px x 200px
    def save(self, **kwargs):
        # Ghi đè phương thức save()
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 200:
            output_size = (300, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)