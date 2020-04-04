from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal
from PIL import Image
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Docatago(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
	    verbose_name = 'Category'
	    verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) # set the slug explicitly
        super(Docatago, self).save(*args, **kwargs) # call Django's save()

class Document(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True)
    like = models.ManyToManyField(User, blank=True, related_name='docs_likes')
    link_url = models.URLField(max_length=255)
    credit = models.DecimalField(max_digits=8, decimal_places=0, default=Decimal('0'))
    catago = models.ForeignKey(Docatago, on_delete=models.CASCADE, verbose_name = "Category")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) # set the slug explicitly
        super(Document, self).save(*args, **kwargs) # call Django's save()
    
    # def get_absolute_url(self):
    #     return reverse("quiz-detail", kwargs={"slug": self.slug})

    # def get_like_url(self):
    #     return reverse("quiz-like", kwargs={"slug": self.slug})

    # def get_api_like_url(self):
    #     return reverse("quiz-api-like", kwargs={"slug": self.slug})

    # Ghi đè hàm save() đẻ chỉnh kích thước ảnh xuống 300px x 200px
    def save(self, **kwargs):
        # Ghi đè phương thức save()
        super().save()
        img = Image.open(self.image.path)
        if img.height > 750 or img.width > 450:
            output_size = (750, 450)
            img.thumbnail(output_size)
            img.save(self.image.path)