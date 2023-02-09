from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('map/',views.map, name='map'),
    path('about-us/', views.about_us, name='about-us'),
    path('basic_table/', views.blank, name='basic_table'),
    path('covisu/', views.covisu, name='covisu'),
    path('gephi/', views.gephi, name='gephi'),
    path('datamine/', views.datamine, name='datamine'),
    path('map_sample/',views.map_sample, name='map_sample'),
]
