from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Nurse

@receiver(post_save,sender=Nurse)
def example(sender,instance,created,**kwargs):
    if created:
        print("Instance is saved  " + instance.role)
