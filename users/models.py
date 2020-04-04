from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from decimal import Decimal
from PIL import Image

# Create your models here.
# Hàm tạo profile cho tài khoản
class Profile(models.Model):

    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]

    PREMIUM = 'PREM'
    FREE = 'FREE'

    PREMIUM_STATUS = [
        (FREE, 'Free'),
        (PREMIUM, 'Premium'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    acc_type = models.CharField(max_length=4, choices=PREMIUM_STATUS, default=FREE, verbose_name = "Account type")
    credit = models.DecimalField(max_digits=8, decimal_places=0, default=Decimal('0'))
    phone = PhoneNumberField(unique=True, verbose_name = "Phone number")
    objects = models.Manager()

    def __str__(self):
        return f'{self.user.username} Profile'

    # Ghi đè hàm save() đẻ chỉnh kích thước ảnh xuống 200px
    def save(self, **kwargs):
        # Ghi đè phương thức save()
        super().save()
        img = Image.open(self.image.path)
        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)
