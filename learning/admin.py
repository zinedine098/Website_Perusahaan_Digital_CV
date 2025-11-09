from django.contrib import admin
from .models import Enrollment, LessonProgress, CourseProgress, Review

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at', 'is_active']
    list_filter = ['is_active', 'enrolled_at']
    search_fields = ['student__username', 'course__title']

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'lesson', 'is_completed', 'progress_percentage', 'completed_at']
    list_filter = ['is_completed', 'completed_at']

@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'progress_percentage', 'completed_lessons', 'total_lessons']
    list_filter = ['progress_percentage']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['student__username', 'course__title', 'comment']