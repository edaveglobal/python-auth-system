from django.contrib import admin
from .models import UserVerified

class UserVerifiedAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_user_verified', 'verified_at', 'updated_at')
    
admin.site.register(UserVerified, UserVerifiedAdmin)