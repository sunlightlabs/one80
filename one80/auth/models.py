import md5

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models, transaction
from social_auth.signals import socialauth_registered
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, default='')
    is_complete = models.BooleanField(default=False, editable=False)

    class Meta:
        app_label = 'auth'

    def __unicode__(self):
        return self.user.__unicode__()

    @property
    def avatar(self):
        provider = self.provider
        try:
            if provider == 'facebook':
                return 'http://graph.facebook.com/%s/picture' % self.user.social_auth.all()[0].uid
            elif provider == 'twitter':
                return 'http://tweetimag.es/i/%s_n' % self.user.username
        except (AttributeError, IndexError):
            pass

        emailhash = md5.new(self.email.lower()).hexdigest()
        return 'http://www.gravatar.com/avatar/%s?default=identicon' % emailhash

    @property
    def email(self):
        return self.user.email

    @email.setter
    def email(self, value):
        self.user.email = value
        self.user.save()

    @property
    def provider(self):
        try:
            return self.user.social_auth.all()[0].provider
        except (AttributeError, IndexError):
            return None

def userprofile_save_handler(sender, instance, created, **kwargs):
    # fetching user The Hard Way as a hack to force-skip memoization
    user = User.objects.get(pk=instance.user_id)
    if (user.email or instance.phone) and not instance.is_complete:
        instance.is_complete = True
        instance.save()
    elif not (user.email or instance.phone) and instance.is_complete:
        instance.is_complete = False
        instance.save()

def new_users_handler(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = UserProfile.objects.create(user=user)
        if user.email:
            profile.is_complete = True

        profile.save()

post_save.connect(userprofile_save_handler, sender=UserProfile)
post_save.connect(new_users_handler, sender=User)