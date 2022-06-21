from django.urls import path

from . import views

app_name = 'books'
urlpatterns = [
    path('books', views.ReadBookAPIViews.as_view()),
    path('books/<int:id>', views.ReadBookAPIViews.as_view()),
    path('books/create', views.CreateBookAPIViews.as_view()),
    path('books/update/<int:id>', views.UpdateBookAPIViews.as_view()),
    path('books/delete/<int:id>', views.DeleteBookAPIViews.as_view()),
]