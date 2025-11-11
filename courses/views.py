from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from .models import Course, Category, Module, Lesson, HomePageHero, HomePageFeature, HomePageFloatingCard, Instructor, HomePageCTA
from .forms import CourseForm, ModuleForm, LessonForm


def home(request):
    """Halaman beranda"""
    featured_courses = Course.objects.filter(is_published=True)[:6]  # Ambil 6 kursus terbaru
    
    # Get or create a default HomePageHero instance
    hero_data, created = HomePageHero.objects.get_or_create(
        id=1,  # Using a fixed ID to ensure we always get the same instance
        defaults={
            'title': 'Transform Your Future with Expert-Led Online Courses',
            'subtitle': 'Discover thousands of high-quality courses designed by industry professionals. Learn at your own pace, gain in-demand skills, and advance your career from anywhere in the world.',
        }
    )
    
    # Get home page features
    home_features = HomePageFeature.objects.all().order_by('order')
    
    # Get floating cards
    floating_cards = list(HomePageFloatingCard.objects.all().order_by('order'))
    
    # Get featured instructors
    featured_instructors = Instructor.objects.all().order_by('order')
    
    # Get CTA section data
    cta_data, created = HomePageCTA.objects.get_or_create(
        id=1,  # Using a fixed ID to ensure we always get the same instance
        defaults={
            'title': 'Transform Your Future with Expert-Led Online Courses',
            'subtitle': 'Join thousands of successful learners who have advanced their careers through our comprehensive online education platform.',
        }
    )

    context = {
        'featured_courses': featured_courses,
        'hero_data': hero_data,
        'home_features': home_features,
        'floating_cards': floating_cards,
        'featured_instructors': featured_instructors,
        'cta_data': cta_data,
    }
    return render(request, 'home.html', context)
def about(request):
    """Halaman about"""
    return render(request, 'about.html')


def course_list(request):
    """Menampilkan semua kursus yang tersedia"""
    courses = Course.objects.filter(is_published=True)
    categories = Category.objects.all()
    
    category_filter = request.GET.get('category')
    if category_filter:
        courses = courses.filter(category__id=category_filter)
    
    search_query = request.GET.get('search')
    if search_query:
        courses = courses.filter(title__icontains=search_query)
    
    context = {
        'courses': courses,
        'categories': categories,
        'selected_category': category_filter,
        'search_query': search_query,
    }
    return render(request, 'courses/course_list.html', context)


def course_detail(request, slug):
    """Menampilkan detail kursus"""
    course = get_object_or_404(Course, slug=slug, is_published=True)
    modules = course.modules.all()
    
    context = {
        'course': course,
        'modules': modules,
    }
    return render(request, 'courses/course_detail.html', context)


@login_required
def course_create(request):
    """Membuat kursus baru (untuk instruktur)"""
    if request.user.role != 'instructor':
        messages.error(request, 'Hanya instruktur yang dapat membuat kursus.')
        return redirect('course_list')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Kursus berhasil dibuat.')
            return redirect('course_detail', slug=course.slug)
    else:
        form = CourseForm()
    
    return render(request, 'courses/course_form.html', {'form': form})


@login_required
def course_edit(request, slug):
    """Mengedit kursus (untuk instruktur yang membuat)"""
    course = get_object_or_404(Course, slug=slug)
    
    if request.user != course.instructor and not request.user.is_staff:
        messages.error(request, 'Anda tidak memiliki izin untuk mengedit kursus ini.')
        return redirect('course_detail', slug=course.slug)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kursus berhasil diperbarui.')
            return redirect('course_detail', slug=course.slug)
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courses/course_form.html', {'form': form, 'course': course})


@login_required
def enroll_course(request, slug):
    """Mendaftarkan siswa ke kursus"""
    course = get_object_or_404(Course, slug=slug, is_published=True)
    
    if request.user.role != 'student':
        messages.error(request, 'Hanya siswa yang dapat mendaftar ke kursus.')
        return redirect('course_detail', slug=course.slug)
    
    # Mengecek apakah pengguna sudah terdaftar
    from learning.models import Enrollment
    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )
    
    if created:
        messages.success(request, f'Anda berhasil terdaftar di kursus {course.title}.')
    else:
        messages.info(request, f'Anda sudah terdaftar di kursus {course.title}.')
    
    return redirect('course_detail', slug=course.slug)


@login_required
def module_create(request, course_slug):
    """Membuat modul untuk kursus (untuk instruktur)"""
    course = get_object_or_404(Course, slug=course_slug)
    
    if request.user != course.instructor and not request.user.is_staff:
        messages.error(request, 'Anda tidak memiliki izin untuk menambahkan modul ke kursus ini.')
        return redirect('course_detail', slug=course.slug)
    
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            messages.success(request, 'Modul berhasil ditambahkan.')
            return redirect('course_detail', slug=course.slug)
    else:
        form = ModuleForm()
    
    return render(request, 'courses/module_form.html', {'form': form, 'course': course})


@login_required
def lesson_create(request, module_id):
    """Membuat pelajaran untuk modul (untuk instruktur)"""
    module = get_object_or_404(Module, id=module_id)
    course = module.course
    
    if request.user != course.instructor and not request.user.is_staff:
        messages.error(request, 'Anda tidak memiliki izin untuk menambahkan pelajaran ke modul ini.')
        return redirect('course_detail', slug=course.slug)
    
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()
            messages.success(request, 'Pelajaran berhasil ditambahkan.')
            return redirect('course_detail', slug=course.slug)
    else:
        form = LessonForm()
    
    return render(request, 'courses/lesson_form.html', {'form': form, 'module': module, 'course': course})