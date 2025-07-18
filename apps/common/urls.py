from django.urls import path
from . import views

urlpatterns = [
    path('destinations/', views.destinations_view, name='destinations'),
    path('languages/', views.languages_view, name='languages'),
    path('tour-types/', views.tour_types_view, name='tour-types'),
    path('timezones/', views.timezones_view, name='timezones'),
]
