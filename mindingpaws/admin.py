from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Minder, Booking
from .forms import MinderCreationForm, BookingCreationForm


class CustomUserAdmin(UserAdmin):
    """
    Custom User admin configuration.

    This admin configuration class customizes the User admin interface.
    It defines add_fieldsets, fieldsets, search_fields, list_display,
    and list_filter settings.
    """

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'email', 'password1',
                       'password2', 'role', 'pet_name', 'pet_species'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password', 'name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    search_fields = ['username', 'name', 'email', 'role']
    list_display = ('username', 'name', 'email', 'role')
    list_filter = ('role',)


class CustomMinderAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for Minder model.

    This admin configuration class customizes the display, search,
    and form behavior for the Minder model in the admin interface.
    """

    def user_name(self, obj):
        """Return name connected to Minder User for list_display."""
        return obj.user.name

    def user_username(self, obj):
        """Return username connected to Minder User for list_display."""
        return obj.user.username

    user_name.short_description = 'Name'
    user_username.short_description = 'Username'

    search_fields = ['user__name', 'user__username']
    list_display = ('user_name', 'user_username', 'bio', 'usual_availability')


class CustomBookingAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for Booking model.

    This admin configuration class customizes the display, search,
    and form behavior for the Booking model in the admin interface.
    """

    fieldsets = (
        ('Users Information', {
            'fields': ('pet_owner', 'pet_owner_name', 'minder', 'minder_name'),
        }),
        ('Booking Information', {
            'fields': ('start_date', 'end_date', 'status',
                       'service_description', 'pet_name', 'pet_species')
        }),
    )
    readonly_fields = ['pet_owner_name', 'minder_name']
    list_display = ('minder_name', 'pet_owner_name', 'status', 'start_date',
                    'end_date', 'service_description',
                    'pet_name', 'pet_species')
    search_fields = ['pet_owner_name', 'minder_name',
                     'pet_name', 'pet_species']
    list_filter = ('status', 'minder_name', 'pet_owner_name',
                   'pet_name', 'pet_species')
    form = BookingCreationForm


# Register models with custom admin configurations
admin.site.register(User, CustomUserAdmin)
admin.site.register(Minder, CustomMinderAdmin)
admin.site.register(Booking, CustomBookingAdmin)
