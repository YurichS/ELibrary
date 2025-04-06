from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from .tasks import send_notification_email
from django.utils import timezone

# Create your views here.


class ReaderViews(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer


class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=["patch"])
    def borrow(self, request, pk=None):
        book = self.get_object()
        if book.copies > 0:
            book.copies -= 1
            book.save()
            send_notification_email.delay(
                request.user.email,
                "You borrowed a book!",
                f"You have borrowed '{book.title}' on {timezone.now().strftime('%Y-%m-%d %H:%M')}",
            )
            return Response({"message": "Book borrowed successfully."})
        return Response(
            {"error": "No available copies."}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None):
        book = self.get_object()
        book.copies += 1
        book.save()
        send_notification_email.delay(
            request.user.email,
            "You returned a book!",
            f"You have returned '{book.title}' on {timezone.now().strftime('%Y-%m-%d %H:%M')}",
        )
        return Response({"message": "Book returned successfully."})


class BorrowedBookView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get(self, request, reader_id):
        reader = Reader.objects.filter(id=reader_id)
        books = Book.objects.filter(readers=reader).all()
        return Response({"reader": {reader.username}, "books": {books}})
