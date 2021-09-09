from django.contrib import admin

from .models import StockPicture


class StockPictureAdmin(admin.ModelAdmin):
    list_display = ("photo", "kind")


admin.site.register(StockPicture, StockPictureAdmin)
