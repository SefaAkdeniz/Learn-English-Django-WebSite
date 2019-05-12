from django.contrib import admin
from kelime.models import Kelime, KelimeBilgi, TamamlananKelime

# Register your models here.
admin.site.site_header = 'Learn English Admin Panel'


@admin.register(Kelime)
class KelimeAdmin(admin.ModelAdmin):

    list_display = ["engWord", "trWord", "structure"]
    list_display_links = ["engWord", "trWord", "structure"]
    list_filter = ["structure"]
    search_fields = ["engWord", "trWord", "structure"]

    class Meta:
        model = Kelime


@admin.register(KelimeBilgi)
class KelimeBilgiAdmin(admin.ModelAdmin):
    list_display = ["user", "word", "date", "level"]
    list_display_links = ["user", "word", "date", "level"]
    list_filter = ["user", "word", "date", "level"]

    class Meta:
        model = KelimeBilgi

@admin.register(TamamlananKelime)
class TamamlananKelimeAdmin(admin.ModelAdmin):
    list_display = ["user", "word", "date"]
    list_display_links = ["user", "word", "date"]
    list_filter = ["user", "word", "date"]

    class Meta:
        model = TamamlananKelime
