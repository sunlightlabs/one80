from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.utils.safestring import mark_safe

from one80.auth.models import UserProfile

def complete_profile_required(view):
    '''Ensure that a user has completed their profile before returning
       the requested resource. Otherwise, redirect to the profile page with
       an appropriate flash message.'''

    @wraps(view)
    def inner(request, *args, **kwargs):
        user = request.user

        # if the user is logged out, they have no profile to complete.
        if user.is_authenticated():
            try:
                complete = user.profile.is_complete
            except UserProfile.DoesNotExist:
                complete = False

            if not complete:
                messages.info(request, settings.COMPLETE_PROFILE_MESSAGE)
                return redirect('profile', next=request.path_info)

        return view(request, *args, **kwargs)

    return inner

def return_after_login(view):
    '''Mark a view as redirectable -- that is, people logging in from here will want to
       come back rather than go to the profile page'''

    @wraps(view)
    def inner(request, *args, **kwargs):
        request.session['next'] = request.path_info

        return view(request, *args, **kwargs)

    return inner