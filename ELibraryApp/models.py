from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date, timedelta


# Create your models here.
class Reader(AbstractUser):
    class Meta:
        verbose_name = "Raeder"
        verbose_name_plural = "Readers"


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    readers = models.ForeignKey(Reader, on_delete=models.CASCADE)
    days_for_reading = models.PositiveIntegerField(default=7)
    copies = models.PositiveIntegerField(default=0)


class DateToReturn(models.Model):
    reader = models.ForeignKey("Reader", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    return_date = models.DateField()

    def get_days_for_reading(self):
        return self.book.days_for_reading

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.return_date = date.today() + timedelta(days=self.get_days_for_reading())
