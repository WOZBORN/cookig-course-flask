from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.courses_view, name='courses'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/', views.course_detail, name='lesson_detail'),
]
