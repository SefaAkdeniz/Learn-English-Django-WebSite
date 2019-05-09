from django.contrib import admin
from kelime.models import Kelime, KelimeBilgi

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
