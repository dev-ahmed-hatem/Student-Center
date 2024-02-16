from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Teacher)
admin.site.register(Lesson)
admin.site.register(Appendix)
