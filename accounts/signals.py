from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import UserProfile, User


# AFTER SAVING OR UPDATE
@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print("User profile is created")
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print("User is updated")
        except: 
            # Created the user profile if not exist
            UserProfile.objects.create(user=instance)
            print("Profile was not exist, but i create a new one")
        print("User is updated")

# BEFORE SAVING
@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    print(instance.username, "This user is being saved")
    