from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal
from PIL import Image
from django.urls import reverse
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, verbose_name = "Clean URL")

    def __str__(self):
        return f'{self.title}'

    class Meta:
	    verbose_name = 'Category'
	    verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if self.slug is None:
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
    backup_link = models.URLField(max_length=255, null=True, blank=True, unique=True, verbose_name = "Backup link")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(default='hushare-default.png', null=True)
    # like = models.ManyToManyField(User, blank=True, related_name='docs_likes')
    credit = models.DecimalField(max_digits=8, decimal_places=0, default=Decimal('0'))
    publish = models.BooleanField(blank=True, default=False, verbose_name="Publish",help_text="If yes, the material is displayed in the material list")
    create_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('doc-detail', kwargs={'slug': self.slug})
    
    # def get_absolute_url(self):
    #     return reverse("quiz-detail", kwargs={"slug": self.slug})

    # def get_like_url(self):
    #     return reverse("quiz-like", kwargs={"slug": self.slug})

    # def get_api_like_url(self):
    #     return reverse("quiz-api-like", kwargs={"slug": self.slug})

    def save(self, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 750 or img.width > 450:
            output_size = (750, 450)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ForeignKey(Document, on_delete=models.CASCADE, verbose_name = "Items")
    create_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(verbose_name = "Comment content")
    create_at = models.DateTimeField(auto_now=False, auto_now_add=True)

@receiver(pre_save, sender=Document)
def slugify_title(sender, instance, *args, **kwargs):
    if instance.slug is None:
        instance.slug = slugify(instance.title)
