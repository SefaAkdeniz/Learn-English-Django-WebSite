from django.db import models

# Create your models here.
class Kelime(models.Model):
    engWord = models.CharField(max_length=25,verbose_name="İngilizce")
    trWord= models.CharField(max_length=25,verbose_name="Türkçe")
    sentence = models.TextField(verbose_name="Cümle")
    structure = models.CharField(max_length=25,verbose_name="Yapısı")
    def __str__(self):
        return self.engWord

class KelimeBilgi(models.Model):
    word=models.ForeignKey(Kelime,on_delete = models.CASCADE,verbose_name ="Kelime")
    user=models.ForeignKey("auth.User",on_delete = models.CASCADE,verbose_name ="Kullanıcı")
    date = models.DateTimeField(verbose_name= "Sorulacak Tarih")
    level=models.IntegerField(verbose_name="Seviyesi")