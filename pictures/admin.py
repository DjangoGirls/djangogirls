from django.contrib import admin

from .models import StockPicture


@admin.register(StockPicture)
class StockPictureAdmin(admin.ModelAdmin):
    list_display = ("photo", "kind")
