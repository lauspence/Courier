from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    

class Courier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    vehicle_type = models.CharField(
        max_length=50, 
        choices=[('bike', 'Bike'), ('truck', 'Truck')],
        default='bike'
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class CourierProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)  # Address field
    vehicle_type = models.CharField(max_length=100, null=True, blank=True)  # Vehicle type
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  # Profile picture
    created_at = models.DateTimeField(auto_now_add=True)
    is_courier = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Job(models.Model):
    TRANSPORT_ITEMS = [
        ('furniture', 'Furniture'),
        ('household', 'Household Items'),
        ('electronics', 'Electronics'),
        ('documents', 'Documents'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="jobs")
    courier = models.ForeignKey('Courier', on_delete=models.SET_NULL, null=True, blank=True, related_name="jobs")
    item_type = models.CharField(max_length=50, choices=TRANSPORT_ITEMS)

    # Location data
    pickup_lat = models.FloatField()
    pickup_lng = models.FloatField()
    delivery_lat = models.FloatField(null=True, blank=True)  
    delivery_lng = models.FloatField(null=True, blank=True)
    pickup_location = models.CharField(max_length=255, blank=True, null=True)
    delivery_location = models.CharField(max_length=255, blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Job {self.id}: {self.item_type} by {self.customer.user.username}"


class DeliveryHistory(models.Model):
    courier = models.ForeignKey(Courier, related_name='delivery_history', on_delete=models.CASCADE)
    job = models.ForeignKey(Job, related_name='delivery_history', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=Job.STATUS_CHOICES)
    completed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.courier.user.first_name} {self.courier.user.last_name} - Job {self.job.id} completed at {self.completed_at}"

