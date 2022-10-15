from django.urls import path
from .views import ReviewView,add_review 

urlpatterns = [
    path('review/',ReviewView.as_view(), name="review"),
    path('add_review/<int:id>',add_review, name="add_review"),
]   
