from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
     
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    display_name = models.CharField(max_length=50)

    @models.permalink
    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
        
def user_post_save(sender, instance, signal, *args, **kwargs):
    """
    On user creation, create the associated UserProfile object and fill
    it with reasonable default values.
    """
   
    profile, new = UserProfile.objects.get_or_create(user=instance)
    if new:
        if profile.user.first_name and profile.user.last_name:
            profile.display_name = "%s %s." % (profile.user.first_name, profile.user.last_name[0])
        else:
            profile.display_name = profile.user.username
        profile.save()    
signals.post_save.connect(user_post_save, sender=User)