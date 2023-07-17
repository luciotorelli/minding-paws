from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Minder, Booking
from .forms import MinderCreationForm, BookingCreationForm


class CustomUserAdmin(UserAdmin):
    # Add fields to the 'Add User page'.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role', 'pet_name', 'pet_species'),
        }),
    )

    # Set up the order and which fields to display in the 'Edit User page'.
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'role'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )

    search_fields = ['username', 'first_name', 'last_name', 'email', 'role']
    list_display = ('username', 'first_name', 'last_name', 'email', 'role')
    list_filter = ('role',)


class CustomMinderAdmin(admin.ModelAdmin):
    def user_name(self, obj):
        """user_name

        Returns the name connected to the Minder User to be used on list_display

        Returns:
            object: name of the user
        """
        return obj.user.name

    def user_username(self, obj):
        """user_username

        Returns the username connected to the Minder User to be used on list_display

        Returns:
            object: username of the user
        """
        return obj.user.username

    # Rename the user and username list display for better semantics.
    user_name.short_description = 'Name'
    user_username.short_description = 'Username'

    search_fields = ['user__name', 'user__username']
    list_display = ('user_name', 'user_username', 'bio', 'usual_availability')
    form = MinderCreationForm


class CustomBookingAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Users Information', {
            'fields': ('pet_owner_user', 'pet_owner_name', 'minder', 'minder_name'),
        }),
        ('Booking Information', {
            'fields': ('start_date', 'end_date', 'status', 'service_description', 'pet_name', 'pet_species')
        }),

    )
    readonly_fields = ['pet_owner_name', 'minder_name']
    list_display = ('minder_name', 'pet_owner_name', 'status', 'start_date',
                    'end_date', 'service_description', 'pet_name', 'pet_species')
    search_fields = ['pet_owner_name',
                     'minder_name', 'pet_name', 'pet_species']
    list_filter = ('status', 'minder_name', 'pet_owner_name',
                   'pet_name', 'pet_species')
    form = BookingCreationForm


admin.site.register(User, CustomUserAdmin)
admin.site.register(Minder, CustomMinderAdmin)
admin.site.register(Booking, CustomBookingAdmin)
