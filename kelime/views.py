from django.shortcuts import render,redirect
from kelime.models import Kelime,KelimeBilgi
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta

# Create your views here.
def index(request):
    return render(request,"index.html")
  

@login_required(login_url = "user:login")
def question(request):   
    cevap=request.GET.get("answer")
    soru=request.GET.get("soru")    
    if cevap:
        dogru=Kelime.objects.filter(engWord=soru).first()    
        if dogru.trWord.upper()==cevap.upper():
            messages.success(request,"Tebrikler! Doğru Bildiniz.")
            Kayit=KelimeBilgi(user=request.user,word=dogru,level=1,date=timezone.now() + timedelta(days=1)+timedelta(hours=3))
            Kayit.save()
        else:
            messages.info(request,"Tüh! Yanlış Cevap.")
    
    control=True
    while control:
        kelime = Kelime.objects.order_by("?").first()
        count = KelimeBilgi.objects.filter(word=kelime,user=request.user).count()
        if(count==0):
            control=False      
        kelimeSayisi=Kelime.objects.all().count()
        kayitliVeri=KelimeBilgi.objects.filter(user=request.user).count()
        if kelimeSayisi==kayitliVeri:
            messages.success(request,"Tebrikler! Tüm Kelimeleri Bildiniz")
            return redirect("index")
    return render(request,"question.html",{"kelime":kelime})


@login_required(login_url = "user:login")
def testing(request):
    count=KelimeBilgi.objects.filter(user=request.user).count()
    if count==0:
        messages.info(request,"İlk Öncelikle Kelime Öğrenmelisiniz")
        return redirect("index")
    cevap=request.GET.get("answer")
    soru=request.GET.get("soru") 
    if cevap:
        dogru=Kelime.objects.filter(engWord=soru).first()
        kayit=KelimeBilgi.objects.filter(user=request.user,word_id=dogru.id).first()  
        if dogru.trWord.upper()==cevap.upper():
            messages.success(request,"Tebrikler! Doğru Bildiniz.")          
            if kayit.level==1:
                kayit.level=2
                kayit.date=datetime.now() + timedelta(weeks=1)
                kayit.save()
            elif kayit.level==2:
                kayit.level=3
                kayit.date=datetime.now() + timedelta(days=30)
                kayit.save()
            elif kayit.level==3:
                kayit.level=4
                kayit.date=datetime.now() + timedelta(days=180)
                kayit.save()               
            elif kayit.level==4:
                kayit.level=5
                kayit.date=datetime.now() + timedelta(days=999)
                kayit.save()
        else:
            messages.info(request,"Tüh! Yanlış Cevap.")
            kayit.level=1
            kayit.date=timezone.now() + timedelta(days=1)+timedelta(hours=3)
            kayit.save() 
    id=KelimeBilgi.objects.filter(user=request.user).order_by("date").first()        
    kelime=Kelime.objects.filter(id=id.word_id).first()
    if  id.date.toordinal() > datetime.now().toordinal():
        messages.success(request,"Şuanlık Testedilecek Kelimeniz Yok")
        return redirect("index")     
    return render(request,"testing.html",{"kelime":kelime})

@login_required(login_url = "user:login")
def statistics(request):
    return render(request,"statistics.html")