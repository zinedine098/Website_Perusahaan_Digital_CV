from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class Course(models.Model):
    DIFFICULTY_CHOICES = (
        ('beginner', 'Pemula'),
        ('intermediate', 'Menengah'),
        ('advanced', 'Lanjutan'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)    
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duration = models.IntegerField(help_text="Durasi kursus dalam jam")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})
    
    def get_enrollment_count(self):
        return self.enrollments.count()


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    LESSON_TYPE_CHOICES = (
        ('video', 'Video'),
        ('text', 'Teks'),
        ('quiz', 'Kuis'),
        ('assignment', 'Tugas'),
    )
    
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES, default='text')
    video_url = models.URLField(blank=True, help_text="URL embed video dari YouTube/Vimeo")
    duration = models.IntegerField(help_text="Durasi pelajaran dalam menit", default=0)
    order = models.PositiveIntegerField(default=1)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.module.title} - {self.title}"