from django.conf import settings

def authentication_services(request):
    return {'authentication_services': settings.AUTHENTICATION_SERVICES}