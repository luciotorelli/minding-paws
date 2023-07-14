from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Minder, Booking

admin.site.register(User, UserAdmin)
admin.site.register(Minder)
admin.site.register(Booking)
