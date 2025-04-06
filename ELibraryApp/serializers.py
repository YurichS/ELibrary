from .models import *
from rest_framework import serializers


class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = ("username", "firstname", "lastname", "email")


class ReaderSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Reader
        fields = ("username", "email", "password")


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
