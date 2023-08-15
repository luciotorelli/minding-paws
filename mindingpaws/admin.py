from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Minder, Booking
from .forms import MinderCreationForm, BookingCreationForm


class CustomUserAdmin(UserAdmin):
    """
    Custom User admin configuration.

    This admin configuration class is used to customize the User admin interface.
    It defines the add_fieldsets, fieldsets, search_fields, list_display, and list_filter settings.

    Attributes:
        add_fieldsets (tuple): Defines the fields to display on the 'Add User page'.
        fieldsets (tuple): Defines the order and fields to display on the 'Edit User page'.
        search_fields (list): Fields to use for searching.
        list_display (tuple): Fields to display in the list view.
        list_filter (tuple): Fields to use for filtering in the list view.

    """
    # Add fields to the 'Add User page'.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'email', 'password1', 'password2', 'role', 'pet_name', 'pet_species'),
        }),
    )

    # Set up the order and which fields to display in the 'Edit User page'.
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'name', 'email', 'role'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )

    search_fields = ['username', 'name', 'email', 'role']
    list_display = ('username', 'name', 'email', 'role')
    list_filter = ('role',)


class CustomMinderAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for Minder model.

    This admin configuration class customizes the display, search, and form behavior for the Minder model in the admin interface.

    Methods:
        user_name(obj): Return the name connected to the Minder User for use in list_display.
        user_username(obj): Return the username connected to the Minder User for use in list_display.
        get_form(request, obj=None, **kwargs): Get the form to use for adding/editing a Minder.

    Attributes:
        search_fields (list): Fields to use for searching.
        list_display (tuple): Fields to display in the list view.

    """
    def user_name(self, obj):
        """
        Return the name connected to the Minder User for use on list_display.

        Args:
            obj (Minder): The Minder object.

        Returns:
            str: The name of the user.
        """
        return obj.user.name

    def user_username(self, obj):
        """
        Return the username connected to the Minder User for use on list_display.

        Args:
            obj (Minder): The Minder object.

        Returns:
            str: The username of the user.
        """
        return obj.user.username

    # Rename the user and username list display for better semantics.
    user_name.short_description = 'Name'
    user_username.short_description = 'Username'

    search_fields = ['user__name', 'user__username']
    list_display = ('user_name', 'user_username', 'bio', 'usual_availability')


class CustomBookingAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for Booking model.

    This admin configuration class customizes the display, search, and form behavior for the Booking model in the admin interface.

    Attributes:
        fieldsets (tuple): Defines the fieldsets for the admin detail view.
        readonly_fields (list): Fields that are read-only in the admin interface.
        list_display (tuple): Fields to display in the list view.
        search_fields (list): Fields to use for searching.
        list_filter (tuple): Fields to use for filtering in the list view.
        form: The form to use for adding/editing a Booking.

    """
    fieldsets = (
        ('Users Information', {
            'fields': ('pet_owner', 'pet_owner_name', 'minder', 'minder_name'),
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

# Register models with custom admin configurations
admin.site.register(User, CustomUserAdmin)
admin.site.register(Minder, CustomMinderAdmin)
admin.site.register(Booking, CustomBookingAdmin)
