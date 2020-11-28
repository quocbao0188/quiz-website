from django.db.models.signals import post_save
# from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Wallet, Profile

@receiver(post_save, sender=Profile)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(profile_wallet_id=instance.id)

# @receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
# def save_profile(sender, instance, created, **kwargs):
#     user = instance
#     if created:
#         profile = Profile(user=user)
#         profile.save()

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()