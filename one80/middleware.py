from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.urlresolvers import resolve, Resolver404
from django.shortcuts import redirect
from django.utils.safestring import mark_safe

from one80.auth.models import UserProfile

class CompletedProfileMiddleware(object):
    '''Ensure that a user has completed their profile before returning
       the requested resource. Otherwise, redirect to the profile page with
       an appropriate flash message.
       '''

    def process_request(self, request):
        user = request.user

        if user.is_authenticated():
            try:
                complete = user.profile.is_complete
            except UserProfile.DoesNotExist:
                complete = False

            try:
                loc = resolve(request.path_info)
            except Resolver404:
                return

            if not complete and not request.path_info.startswith('/static') and not request.path_info.startswith('/media'):
                # don't redirect if we're already on the profile page, or are logging out
                if loc.url_name in ['profile', 'logout'] or loc.app_name == 'admin':
                    if loc.url_name == 'profile':
                        messages.info(request, settings.COMPLETE_PROFILE_MESSAGE)
                    if loc.app_name == 'admin':
                        messages.warning(request, settings.ADMIN_COMPLETE_PROFILE_MESSAGE)

                    return

                #no exemptions matched, head to the profile page
                request.session['next'] = request.path_info
                request.session['was_redirected_from_completed_profile_middleware'] = True
                return redirect('profile')
