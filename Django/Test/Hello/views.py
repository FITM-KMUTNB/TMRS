from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request,*args, **kwargs):
    print(args, kwargs)
    print(request.user)
    #return HttpResponse("<h1>eiei</h1>")
    return render(request, "index.php",{})
