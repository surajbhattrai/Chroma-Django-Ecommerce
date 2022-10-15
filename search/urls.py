from django.urls import path
from search import views

urlpatterns = [
    path('search/', views.SearchView.as_view(), name='search'),
]      