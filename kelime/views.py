from django.shortcuts import render,redirect
from kelime.models import Kelime,KelimeBilgi
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,"index.html")

@login_required(login_url = "user:login")
def question(request):
    
    cevap=request.GET.get("answer")
    soru=request.GET.get("soru")  
    
    if cevap:
        dogru=Kelime.objects.filter(engWord=soru).first()
        
        print(dogru)
        print(cevap)
        print(soru)
        

        
        if dogru.trWord.upper()==cevap.upper():
            messages.success(request,"Tebrikler Doğru Bildiniz..")
            Kayit=KelimeBilgi(user=request.user,word=dogru,level=1)
            Kayit.save()
        else:
            messages.info(request,"Maalesef Yanlış Yaptınız..")
    
    control=True
    while control:
        kelime = Kelime.objects.order_by("?").first()
        count = KelimeBilgi.objects.filter(word=kelime,user=request.user).count()
        if(count==0):
            control=False
        
        kelimeSayisi=Kelime.objects.all().count()
        kayitliVeri=KelimeBilgi.objects.filter(user=request.user).count()

        if kelimeSayisi==kayitliVeri:
            messages.info(request,"Kelime Kalmadı")
            return redirect("index")

    return render(request,"question.html",{"kelime":kelime})