from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from decimal import Decimal
from django.utils import timezone
from PIL import Image

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
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=OTHER)
    acc_type = models.CharField(max_length=4, choices=PREMIUM_STATUS, default=FREE, verbose_name = "Account type")
    # credit = models.DecimalField(max_digits=8, decimal_places=0, default=Decimal('0'))
    phone = PhoneNumberField(verbose_name = "Phone number", null=True, blank=True, unique=True)
    student_id = models.BigIntegerField(unique=True)
    faculty = models.CharField(max_length=50)
    birthday = models.DateField(default=timezone.now)
    objects = models.Manager()

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Wallet(models.Model):
    profile_wallet = models.OneToOneField(Profile, on_delete=models.CASCADE)
    credit = models.DecimalField(max_digits=8, decimal_places=0, default=Decimal('0'))
    create_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f'{self.profile_wallet.user.username} Wallet'