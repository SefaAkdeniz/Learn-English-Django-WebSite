from django.shortcuts import render, redirect
from kelime.models import Kelime, KelimeBilgi, TamamlananKelime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils import formats

# Create your views here.

def index(request):

    return render(request, "index.html")


@login_required(login_url="user:login")
def question(request):

    cevap = request.GET.get("answer")
    soru = request.GET.get("soru")
    
    if cevap:
        dogru = Kelime.objects.filter(engWord=soru).first()
        if dogru.trWord.upper() == cevap.upper():
            messages.success(request, "Tebrikler! Doğru Bildiniz.")
            Kayit = KelimeBilgi(user=request.user, word=dogru, level=1, date=timezone.now(
            ) + timedelta(days=1)+timedelta(hours=3))
            Kayit.save()
            return redirect("question")
        else:
            messages.info(request, "Tüh! Yanlış Cevap.")

    control = True
    while control:
        kelime = Kelime.objects.order_by("?").first()
        inProgressCount = KelimeBilgi.objects.filter(word=kelime, user=request.user).count()
        doneCount = TamamlananKelime.objects.filter(word=kelime, user=request.user).count()
        if inProgressCount == 0 and doneCount == 0:
            control = False

        kelimeSayisi = Kelime.objects.all().count()
        kayitliVeri = KelimeBilgi.objects.filter(user=request.user).count()
        tamamlananVeri = TamamlananKelime.objects.filter(user=request.user).count()
        if kelimeSayisi == kayitliVeri+tamamlananVeri:
            messages.success(request, "Tebrikler! Tüm Kelimeleri Bildiniz")
            return redirect("index")

        oran = ((kayitliVeri+tamamlananVeri)*100)/kelimeSayisi
        oran = int(oran)

    return render(request, "question.html", {"kelime": kelime, "oran": oran, "kelimeSayisi": kelimeSayisi, "kayitliVeri": kayitliVeri})


@login_required(login_url="user:login")
def testing(request):

    count = KelimeBilgi.objects.filter(user=request.user).count()
    if count == 0:
        messages.info(request, "İlk Öncelikle Kelime Öğrenmelisiniz")
        return redirect("index")

    cevap = request.GET.get("answer")
    soru = request.GET.get("soru")
    if cevap:
        dogru = Kelime.objects.filter(engWord=soru).first()
        kayit = KelimeBilgi.objects.filter(
            user=request.user, word_id=dogru.id).first()
        if dogru.trWord.upper() == cevap.upper():
            messages.success(request, "Tebrikler! Doğru Bildiniz.")
            if kayit.level == 1:
                kayit.level = 2
                kayit.date = datetime.now() + timedelta(weeks=1)
                kayit.save()
            elif kayit.level == 2:
                kayit.level = 3
                kayit.date = datetime.now() + timedelta(days=30)
                kayit.save()
            elif kayit.level == 3:
                kayit.level = 4
                kayit.date = datetime.now() + timedelta(days=180)
                kayit.save()
            elif kayit.level == 4:
                messages.success(request, "Tebrikler! " +soru + " Kelimesini Ezberlediniz.")
                Tamamlanan = TamamlananKelime(
                    user=request.user, word=dogru, date=timezone.now())
                Tamamlanan.save()
                kayit.delete()
        else:
            messages.info(request, "Tüh! Yanlış Cevap.")
            kayit.level = 1
            kayit.date = timezone.now() + timedelta(days=1)+timedelta(hours=3)
            kayit.save()

    count = KelimeBilgi.objects.filter(user=request.user).count()
    if count == 0:
        return redirect("index")

    id = KelimeBilgi.objects.filter(user=request.user).order_by("date").first()
    kelime = Kelime.objects.filter(id=id.word_id).first()
    if id.date.toordinal() > datetime.now().toordinal():
        messages.success(request, "Şuanlık Testedilecek Kelimeniz Yok")
        return redirect("index")
    return render(request, "testing.html", {"kelime": kelime})


@login_required(login_url="user:login")
def statistics(request):

    yearCount = [0, 0, 0]
    yearName = ["", "", ""]
    for i in range(0, 3):
        yearCount[i] = TamamlananKelime.objects.filter(user=request.user, date__year=int(timezone.now().year)-i).count()
        yearName[i] = str(int(timezone.now().year)-i)

    mountCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, 12):
        mountCount[i] = TamamlananKelime.objects.filter(user=request.user, date__year=timezone.now().year, date__month=1+i).count()

    dayCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, 30):
        dayCount[i] = TamamlananKelime.objects.filter(user=request.user, date__year=timezone.now().year, date__month=timezone.now().month, date__day=1+i).count()

    current = timezone.now()
    current = formats.date_format(current, "DATE_FORMAT")
    current = current.split()
    currentMonth = current[1]
    currentYear = current[2]

    return render(request, "statistics.html", {"yearCount": yearCount, "yearName": yearName, "mountCount": mountCount, "dayCount": dayCount, "currentMonth": currentMonth, "currentYear": currentYear})
