from django.contrib import admin
from .models import Course, Category, Module, Lesson, HomePageHero, HomePageFeature, HomePageFloatingCard, Instructor, HomePageCTA

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    # prepopulated_fields tidak digunakan karena model Category tidak memiliki field slug

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'category', 'difficulty', 'is_published', 'created_at']
    list_filter = ['category', 'difficulty', 'is_published', 'created_at']
    search_fields = ['title', 'instructor__username', 'description']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'lesson_type', 'order', 'is_published']
    list_filter = ['lesson_type', 'is_published', 'module']

@admin.register(HomePageHero)
class HomePageHeroAdmin(admin.ModelAdmin):
    list_display = ['title', 'students_count', 'courses_count', 'success_rate', 'updated_at']
    list_filter = ['created_at', 'updated_at']

@admin.register(HomePageFeature)
class HomePageFeatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']
    ordering = ['order']

@admin.register(HomePageFloatingCard)
class HomePageFloatingCardAdmin(admin.ModelAdmin):
    list_display = ['title', 'student_count', 'order']
    ordering = ['order']

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialty', 'rating', 'course_count', 'student_count', 'order']
    list_filter = ['specialty', 'order']
    search_fields = ['name', 'specialty']

@admin.register(HomePageCTA)
class HomePageCTAAdmin(admin.ModelAdmin):
    list_display = ['title', 'cta_students_count', 'cta_courses_count', 'cta_success_rate', 'updated_at']
    list_filter = ['created_at', 'updated_at']