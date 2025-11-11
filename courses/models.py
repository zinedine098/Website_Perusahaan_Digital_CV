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


class HomePageHero(models.Model):
    """Model for hero section of home page"""
    title = models.CharField(max_length=200, default="Transform Your Future with Expert-Led Online Courses")
    subtitle = models.TextField(default="Discover thousands of high-quality courses designed by industry professionals. Learn at your own pace, gain in-demand skills, and advance your career from anywhere in the world.")
    
    # Stats
    students_count = models.IntegerField(default=50000, help_text="Number of students enrolled")
    courses_count = models.IntegerField(default=1200, help_text="Number of expert courses")
    success_rate = models.IntegerField(default=98, help_text="Success rate percentage")
    
    # Features
    feature_1_title = models.CharField(max_length=100, default="Certified Programs")
    feature_2_title = models.CharField(max_length=100, default="Lifetime Access")
    feature_3_title = models.CharField(max_length=100, default="Expert Instructors")
    
    hero_image = models.ImageField(upload_to='hero_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Home Page Hero"
        verbose_name_plural = "Home Page Heroes"

    def __str__(self):
        return f"Hero Section - {self.title[:50]}..."


class HomePageFeature(models.Model):
    """Model for the three feature boxes on home page"""
    icon_class = models.CharField(max_length=50, help_text="Font Awesome or Bootstrap icon class (e.g., 'fas fa-laptop-code', 'bi bi-shield-check')")
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']
        verbose_name = "Home Page Feature"
        verbose_name_plural = "Home Page Features"

    def __str__(self):
        return self.title


class HomePageFloatingCard(models.Model):
    """Model for floating course cards on home page"""
    ICON_CHOICES = [
        ('bi bi-code-slash', 'Code Slash'),
        ('bi bi-palette', 'Palette'),
        ('bi bi-graph-up', 'Graph Up'),
        ('bi bi-layers', 'Layers'),
        ('bi bi-gem', 'Gem'),
    ]
    
    icon_class = models.CharField(max_length=50, choices=ICON_CHOICES, default='bi bi-code-slash')
    title = models.CharField(max_length=100, help_text="Course category/title")
    student_count = models.IntegerField(default=0, help_text="Number of students for this category")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']
        verbose_name = "Home Page Floating Card"
        verbose_name_plural = "Home Page Floating Cards"

    def __str__(self):
        return self.title


class Instructor(models.Model):
    """Model for instructors featured on home page"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='instructor_profiles/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    course_count = models.IntegerField(default=0)
    student_count = models.IntegerField(default=0)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    dribbble_url = models.URLField(blank=True)
    behance_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']
        verbose_name = "Featured Instructor"
        verbose_name_plural = "Featured Instructors"

    def __str__(self):
        return self.name


class HomePageCTA(models.Model):
    """Model for CTA section on home page"""
    title = models.CharField(max_length=200, default="Transform Your Future with Expert-Led Online Courses")
    subtitle = models.TextField(default="Join thousands of successful learners who have advanced their careers through our comprehensive online education platform.")
    
    # Features
    feature_1 = models.CharField(max_length=200, default="20+ Expert instructors with industry experience")
    feature_2 = models.CharField(max_length=200, default="Certificate of completion for every course")
    feature_3 = models.CharField(max_length=200, default="24/7 access to course materials and resources")
    feature_4 = models.CharField(max_length=200, default="Interactive assignments and real-world projects")
    
    # Stats
    cta_students_count = models.IntegerField(default=15000, help_text="Students enrolled for CTA section")
    cta_courses_count = models.IntegerField(default=150, help_text="Courses available for CTA section")
    cta_success_rate = models.IntegerField(default=98, help_text="Success rate for CTA section")
    
    cta_button_text = models.CharField(max_length=50, default="Browse Courses")
    cta_button_url = models.CharField(max_length=200, default="courses.html")
    secondary_button_text = models.CharField(max_length=50, default="Enroll Now")
    secondary_button_url = models.CharField(max_length=200, default="enroll.html")
    
    cta_image = models.ImageField(upload_to='cta_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Home Page CTA"
        verbose_name_plural = "Home Page CTAs"

    def __str__(self):
        return f"CTA Section - {self.title[:50]}..."