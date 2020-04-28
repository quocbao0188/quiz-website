from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal
from PIL import Image
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, verbose_name = "Clean URL")

    def __str__(self):
        return f'{self.title}'

    class Meta:
	    verbose_name = 'Category'
	    verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) # set the slug explicitly
        super(Category, self).save(*args, **kwargs) # call Django's save()

class Document(models.Model):
    
    DOCUMENT = 'DOC'
    LAB = 'LAB'
    OTHER = 'OTH'

    SPECIES_CHOICES = [
        (DOCUMENT, 'Document'),
        (LAB, 'Practice lab'),
        (OTHER, 'Other'),
    ]

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, verbose_name = "Clean URL")
    species = models.CharField(max_length=3, choices=SPECIES_CHOICES, default=DOCUMENT, verbose_name = "Species")
    catago = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='documents', verbose_name = "Category")
    content = models.TextField(verbose_name = "Description")
    link_url = models.URLField(max_length=255, unique=True, verbose_name = "Direct link")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='hushare-default.png', null=True)
    like = models.ManyToManyField(User, blank=True, related_name='docs_likes')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name = "Date Created")
    credit = models.DecimalField(max_digits=8, decimal_places=0, default=Decimal('0'))
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('doc-detail', kwargs={'slug': self.slug})

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

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Document, blank=True, verbose_name = "Items")
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username