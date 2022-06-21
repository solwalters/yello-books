from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_xml.renderers import XMLRenderer

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .ybXMLRenderer import ybXMLRenderer


class ReadBookAPIViews(APIView):
    renderer_classes = [JSONRenderer, ybXMLRenderer]

    def get(self, request, id=None):
        if id:
            book = get_object_or_404(Book, pk=id)
            serializer = BookSerializer(book)
        else:
            books = Book.objects.all()
            if request.GET is not None:
                # limit search fields to title , description, author
                if request.GET.get('title') is not None:
                    books = books.filter(
                        title__icontains=request.GET.get('title'))
                if request.GET.get('description') is not None:
                    books = books.filter(
                        description__icontains=request.GET.get('description'))
                if request.GET.get('author') is not None:
                    books = books.filter(Q(author__name__icontains=request.GET.get('author')) | Q(
                        author__pseudonym__icontains=request.GET.get('author')))
            serializer = BookSerializer(books, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class CreateBookAPIViews(APIView):
    renderer_classes = [JSONRenderer, ybXMLRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.data['author'] = request.user.id
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UpdateBookAPIViews(APIView):
    renderer_classes = [JSONRenderer, ybXMLRenderer]
    permission_classes = [IsAuthenticated]

    def put(self, request, id=None):
        book = get_object_or_404(Book, pk=id)
        if request.user == book.author:
            request.data['author'] = request.user.id
            serializer = BookSerializer(book, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'success', "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'error', 'data': serializer.errors}, status=status.HTTP_403_FORBIDDEN)


class DeleteBookAPIViews(APIView):
    renderer_classes = [JSONRenderer, ybXMLRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id=None):
        book = get_object_or_404(Book, pk=id)
        if request.user == book.author:
            book.delete()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'details': 'You are not the author of this book.'}, status=status.HTTP_403_FORBIDDEN)
