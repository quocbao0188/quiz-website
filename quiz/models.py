from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Post(models.Model):
    genre = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = models.Manager()
    image = models.ImageField(null=True)

    def __str__(self):
        return self.title

    # Ghi đè hàm save() đẻ chỉnh kích thước ảnh xuống 300px x 200px
    def save(self, **kwargs):
        # Ghi đè phương thức save()
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 200:
            output_size = (300, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)