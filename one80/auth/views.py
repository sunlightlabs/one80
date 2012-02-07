import urlparse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import resolve, Resolver404
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from one80.auth.forms import UserProfileForm
from one80.auth.models import UserProfile

def login_begin(request):

    if request.user.is_anonymous():
        #flag the last page for redirection after login if it was local
        try:
            referer = request.META.get('HTTP_REFERER')
            path = urlparse.urlparse(referer).path
            resolve(path)
            request.session['next'] = path
        except:
            try:
                del request.session['next']
            except:
                pass

        return render(request, 'auth/login.html')
    else:
        return redirect('profile')

def login_complete(request):
    if request.session.get('next'):
        return redirect(request.session['next'])
    else:
        return redirect('index')

def logout_begin(request):
    logout_instructions = ''
    try:
        service = [service for service in settings.AUTHENTICATION_SERVICES if service[0] == request.user.profile.provider][0]
        logout_instructions = mark_safe(' Don\'t forget to <a href="%s" target="_blank">log out of %s</a> too!' % (service[1], service[0]))
    except:
        pass
    messages.info(request, 'You are now logged out.%s' % logout_instructions)
    return redirect('logout_complete')

@login_required
def profile(request):
    user = request.user
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=user)

    form = UserProfileForm(instance=profile)

    if request.POST:
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            success = form.save()
            if success:
                if request.session.get('next') and request.session.get('was_redirected_from_completed_profile_middleware'):
                    storage = messages.get_messages(request)
                    # loop through messages to skip them when we redirect
                    current_messages = [message.message for message in storage]
                    if len(current_messages) == 1:
                        if current_messages[0] not in [settings.COMPLETE_PROFILE_MESSAGE, settings.ADMIN_COMPLETE_PROFILE_MESSAGE]:
                            storage.used = False
                    del request.session['was_redirected_from_completed_profile_middleware']
                    return redirect(request.session.pop('next'))

    data = {
        'user': user,
        'form': form,
    }
    return render(request, 'auth/profile.html', data)
