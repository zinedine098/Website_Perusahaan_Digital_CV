from django.urls import path
from . import views

app_name = 'learning'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('course/<slug:course_slug>/learn/', views.course_learning_view, name='course_learning_view'),
    path('course/<slug:course_slug>/lesson/<int:lesson_id>/', views.lesson_view, name='lesson_view'),
    path('mark-lesson-complete/<int:lesson_id>/', views.mark_lesson_complete, name='mark_lesson_complete'),
    path('course/<slug:course_slug>/review/', views.add_review, name='add_review'),
]