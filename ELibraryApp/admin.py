from django.contrib import admin
from .models import Reader, Book


# Register your models here.
@admin.register(Reader)
class AdminReader(admin.ModelAdmin):
    list_display = ["id", "username", "email"]


@admin.register(Book)
class AdminBook(admin.ModelAdmin):
    list_display = ["id", "title", "days_for_reading", "copies"]
