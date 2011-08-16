from django.shortcuts import render
from one80.committees.models import Hearing

def index(request):
    
    hearings = Hearing.objects.all()
    
    # add filter if user is not staff
    if not request.user.is_staff:
        hearings = hearings.filter(is_public=True)
        
    return render(request, "index.html", {'hearings': hearings})