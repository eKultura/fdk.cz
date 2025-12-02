from django.contrib import admin
from fdk_cz.models import UserProfile

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_vip', 'created_at', 'updated_at')
    list_filter = ('is_vip', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Uživatel', {
            'fields': ('user',)
        }),
        ('VIP Status', {
            'fields': ('is_vip',),
            'description': 'VIP uživatelé mohou vytvořit až 3 aktivní projekty, základní uživatelé jen 1.'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
