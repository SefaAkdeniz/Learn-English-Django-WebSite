from django.shortcuts import render,HttpResponse
from kelime.models import Kelime,KelimeBilgi
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,"index.html")

@login_required(login_url = "user:login")
def question(request):

    control=True

    while control:
        kelime = Kelime.objects.order_by("?").first()
        count = KelimeBilgi.objects.filter(word=kelime,user=request.user).count()
        if(count==0):
            control=False

    return render(request,"question.html",{"kelime":kelime})