from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('courses/', views.course_list, name='course_list'),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('course/create/', views.course_create, name='course_create'),
    path('course/<slug:slug>/edit/', views.course_edit, name='course_edit'),
    path('course/<slug:slug>/enroll/', views.enroll_course, name='enroll_course'),
    path('course/<slug:course_slug>/module/create/', views.module_create, name='module_create'),
    path('module/<int:module_id>/lesson/create/', views.lesson_create, name='lesson_create'),
]