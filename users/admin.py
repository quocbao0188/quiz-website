from django.contrib import admin
from .models import Profile, Wallet
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'gender', 'faculty', 'image', 'phone')

class WalletAdmin(admin.ModelAdmin):
    list_display = ('profile_wallet', 'credit', 'create_at', 'updated_at')
    fieldsets = [
        ("Wallet value", {'fields': ["credit"]})
    ]

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Wallet, WalletAdmin)