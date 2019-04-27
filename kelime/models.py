from django.db import models

# Create your models here.
class Kelime(models.Model):
    engWord = models.CharField(max_length=25,verbose_name="İngilizce")
    trWord= models.CharField(max_length=25,verbose_name="Türkçe")
    sentence = models.TextField(verbose_name="Cümle")
    structure = models.CharField(max_length=25,verbose_name="Yapısı")
    def __str__(self):
        return self.engWord

