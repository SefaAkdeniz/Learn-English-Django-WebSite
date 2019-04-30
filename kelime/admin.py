from django.contrib import admin

from kelime.models import Kelime,KelimeBilgi

admin.site.register(KelimeBilgi)

# Register your models here.
@admin.register(Kelime)
class KelimeAdmin(admin.ModelAdmin):

    list_display=["engWord","trWord","structure"]
    list_display_links=["engWord","trWord","structure"]
    list_filter=["structure"]
    search_fields=["engWord","trWord","structure"]
    class Meta:
        model=Kelime


