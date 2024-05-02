from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, Group
from .models import *


# Register your models here.

class UserProfileAdmin(UserAdmin):
    model = UserProfile
    list_display = ('phone', 'name', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('name', "email")}),
        ('Permissions', {'fields': ('is_staff',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'name', 'email', 'password1', 'password2', 'is_staff'),
        }),
    )
    search_fields = ('phone', 'name', 'email')
    ordering = ('phone',)
    filter_horizontal = ()


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.unregister(Group)

admin.site.register(Teacher)
admin.site.register(Lesson)
admin.site.register(Appendix)
admin.site.register(ContactMessage)
admin.site.register(AccessCode)
