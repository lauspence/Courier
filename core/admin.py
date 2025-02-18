from django.contrib import admin
from .models import Customer, Job, Courier , CourierProfile

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('get_first_name', 'get_last_name', 'get_email', 'phone', 'created_at')
    search_fields = ('get_first_name', 'get_last_name', 'get_email', 'phone')

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'vehicle_type', 'is_available', 'created_at')
    search_fields = ('user__username', 'phone', 'vehicle_type')
    list_filter = ('vehicle_type', 'is_available', 'created_at')


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('customer', 'courier', 'item_type', 'pickup_location', 'delivery_location', 'status', 'created_at')
    list_filter = ('status', 'created_at')  # Replaced 'is_accepted' with 'status'
    search_fields = ('customer__user__username', 'courier__user__username', 'item_type')


# Register CourierProfile (assuming CourierProfile is your profile model)
@admin.register(CourierProfile)  # Make sure to use the correct model name
class CourierProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_courier', 'created_at', 'phone')  # Add any necessary fields here
    search_fields = ('user__username', 'user__email', 'phone')
    list_filter = ('is_courier', 'created_at')  # Filter by courier status and created date
