from django.urls import path
from . import views


urlpatterns=[
    path('', views.index, name='index'),   
    path('search/', views.search_courses, name='search_courses'),
    path('recommend/<int:course_id>/', views.course_recommendations, name='recommend_courses'),
]