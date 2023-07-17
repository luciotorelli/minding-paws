from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Minder, Booking
from .forms import MinderCreationForm, BookingCreationForm

class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role', 'pet_name', 'pet_species'),
        }),
    )

class CustomMinderAdmin(admin.ModelAdmin):
    form = MinderCreationForm

class CustomBookingAdmin(admin.ModelAdmin):
    form = BookingCreationForm

admin.site.register(User, CustomUserAdmin)
admin.site.register(Minder, CustomMinderAdmin)
admin.site.register(Booking, CustomBookingAdmin)
