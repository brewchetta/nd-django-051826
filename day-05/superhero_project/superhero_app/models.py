from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# SUPERHERO #
class Superhero(models.Model):
    alias = models.CharField(max_length=100)
    real_name = models.CharField(max_length=100)
    powers = models.TextField()
    origin_story = models.TextField()
    # user association
    # the user can be null a.k.a. deleted
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="superheroes", null=True, blank=True)

    def __str__(self):
        return self.alias

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# EXTENDED USER #
class UserProfile(models.Model):
    bio = models.TextField(blank=True, null=True)
    favorite_superhero = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    # this is associated one to one with a user, thus "extending" it
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")


from django.db.models.signals import post_save
from django.dispatch import receiver

# receiver says the function below happens after saving a User instance
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **key_word_args):
        # sender is the User model
        # instance is the actual user which got saved
        # created is whether the user was created
        # key_word_args are a safety precaution in case the function gets extra args we won't use
    if created:
        UserProfile.objects.create(user=instance)
    # if user is created, immediately generate a user profile for them