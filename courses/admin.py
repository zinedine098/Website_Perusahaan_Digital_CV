from django.contrib import admin
from .models import Course, Category, Module, Lesson

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