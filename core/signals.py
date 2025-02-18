# core/signals.py
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CourierProfile

@receiver(post_save, sender=User)
def create_courier_profile(sender, instance, created, **kwargs):
    # Ensure that the user is being saved and create the CourierProfile only if needed
    if created:
        # Check if the user has a related CourierProfile and if they are a courier
        if hasattr(instance, 'courierprofile'):
            courier_profile = instance.courierprofile
            if courier_profile.is_courier:
                courier_profile.save()
        else:
            # If no CourierProfile exists, create a new one
            CourierProfile.objects.create(user=instance)
    