from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image

# Create your models here.
# Hàm tạo profile cho tài khoản
class Profile(models.Model):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    gender = models.CharField(max_length=1, null=True, choices=GENDER_CHOICES)
    phone = PhoneNumberField(null=True, blank=False, unique=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.user.username} Profile'

    # Ghi đè hàm save() đẻ chỉnh kích thước ảnh xuống 100px
    def save(self, **kwargs):
        # Ghi đè phương thức save()
        super().save()
        img = Image.open(self.image.path)
        if img.height > 100 or img.width > 100:
            output_size = (100, 100)
            img.thumbnail(output_size)
            img.save(self.image.path)
