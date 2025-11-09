from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from courses.models import Course, Module, Lesson
from .models import Enrollment, LessonProgress, CourseProgress
from .forms import ReviewForm


@login_required
def dashboard(request):
    """Dashboard siswa - menampilkan kursus yang diambil dan progress"""
    if request.user.role != 'student':
        messages.error(request, 'Hanya siswa yang dapat mengakses dashboard.')
        return redirect('home')
    
    # Mendapatkan kursus yang diambil oleh siswa
    enrollments = Enrollment.objects.filter(student=request.user, is_active=True)
    
    # Menghitung progress untuk setiap kursus
    course_progresses = []
    for enrollment in enrollments:
        try:
            progress = enrollment.course_progresses.get(student=request.user)
            course_progresses.append({
                'enrollment': enrollment,
                'progress': progress
            })
        except CourseProgress.DoesNotExist:
            # Jika belum ada progress, buat data progress baru
            total_lessons = enrollment.course.modules.count() * 5  # Perkiraan jumlah pelajaran
            course_progress = CourseProgress.objects.create(
                student=request.user,
                course=enrollment.course,
                enrollment=enrollment,
                total_lessons=total_lessons
            )
            course_progresses.append({
                'enrollment': enrollment,
                'progress': course_progress
            })
    
    context = {
        'course_progresses': course_progresses
    }
    return render(request, 'learning/dashboard.html', context)


@login_required
def course_learning_view(request, course_slug):
    """Menampilkan area pembelajaran untuk kursus tertentu"""
    course = get_object_or_404(Course, slug=course_slug)
    
    # Memastikan siswa terdaftar di kursus ini
    try:
        enrollment = Enrollment.objects.get(student=request.user, course=course)
    except Enrollment.DoesNotExist:
        messages.error(request, 'Anda harus terdaftar di kursus ini untuk mengakses materi pembelajaran.')
        return redirect('course_detail', slug=course_slug)
    
    modules = course.modules.all()
    
    # Mendapatkan progress siswa untuk kursus ini
    try:
        course_progress = CourseProgress.objects.get(student=request.user, course=course)
    except CourseProgress.DoesNotExist:
        # Membuat progress baru jika belum ada
        total_lessons = sum(module.lessons.count() for module in modules)
        course_progress = CourseProgress.objects.create(
            student=request.user,
            course=course,
            enrollment=enrollment,
            total_lessons=total_lessons
        )
    
    context = {
        'course': course,
        'modules': modules,
        'course_progress': course_progress,
    }
    return render(request, 'learning/course_learning.html', context)


@login_required
def lesson_view(request, course_slug, lesson_id):
    """Menampilkan halaman pembelajaran untuk pelajaran tertentu"""
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)
    
    # Memastikan siswa terdaftar di kursus ini
    try:
        enrollment = Enrollment.objects.get(student=request.user, course=course)
    except Enrollment.DoesNotExist:
        messages.error(request, 'Anda harus terdaftar di kursus ini untuk mengakses pelajaran.')
        return redirect('course_detail', slug=course_slug)
    
    # Mendapatkan atau membuat progress pelajaran
    lesson_progress, created = LessonProgress.objects.get_or_create(
        student=request.user,
        lesson=lesson,
        enrollment=enrollment
    )
    
    # Jika pelajaran dilihat untuk pertama kalinya, update progress
    if not lesson_progress.is_completed:
        lesson_progress.is_completed = True
        lesson_progress.progress_percentage = 100
        lesson_progress.save()
        
        # Update progress kursus
        update_course_progress(course, request.user)
    
    context = {
        'course': course,
        'lesson': lesson,
        'lesson_progress': lesson_progress,
    }
    return render(request, 'learning/lesson_view.html', context)


def update_course_progress(course, user):
    """Memperbarui progress keseluruhan kursus untuk seorang siswa"""
    try:
        enrollment = Enrollment.objects.get(student=user, course=course)
        
        # Mendapatkan semua pelajaran dalam kursus ini
        all_lessons = Lesson.objects.filter(module__course=course, is_published=True)
        total_lessons = all_lessons.count()
        
        if total_lessons == 0:
            return
        
        # Menghitung jumlah pelajaran yang sudah selesai
        completed_lessons = LessonProgress.objects.filter(
            student=user,
            lesson__in=all_lessons,
            is_completed=True
        ).count()
        
        # Menghitung persentase progress
        progress_percentage = int((completed_lessons / total_lessons) * 100)
        
        # Mendapatkan atau membuat CourseProgress
        course_progress, created = CourseProgress.objects.get_or_create(
            student=user,
            course=course,
            enrollment=enrollment
        )
        
        # Memperbarui informasi progress
        course_progress.progress_percentage = progress_percentage
        course_progress.completed_lessons = completed_lessons
        course_progress.total_lessons = total_lessons
        course_progress.save()
        
    except Enrollment.DoesNotExist:
        pass


@login_required
def mark_lesson_complete(request, lesson_id):
    """Menandai pelajaran sebagai selesai"""
    if request.method == 'POST':
        lesson = get_object_or_404(Lesson, id=lesson_id)
        
        # Memastikan siswa terdaftar di kursus ini
        try:
            enrollment = Enrollment.objects.get(student=request.user, course=lesson.module.course)
        except Enrollment.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Anda harus terdaftar di kursus ini untuk menyelesaikan pelajaran.'})
        
        # Mendapatkan atau membuat progress pelajaran
        lesson_progress, created = LessonProgress.objects.get_or_create(
            student=request.user,
            lesson=lesson,
            enrollment=enrollment
        )
        
        if not lesson_progress.is_completed:
            lesson_progress.is_completed = True
            lesson_progress.progress_percentage = 100
            lesson_progress.save()
            
            # Update progress kursus
            update_course_progress(lesson.module.course, request.user)
            
            return JsonResponse({'success': True, 'message': 'Pelajaran ditandai sebagai selesai.'})
        
        return JsonResponse({'success': True, 'message': 'Pelajaran sudah ditandai sebagai selesai.'})
    
    return JsonResponse({'success': False, 'message': 'Metode tidak diizinkan.'})


@login_required
def add_review(request, course_slug):
    """Menambahkan ulasan untuk kursus"""
    course = get_object_or_404(Course, slug=course_slug)
    
    if request.method == 'POST':
        # Memastikan siswa terdaftar di kursus ini
        try:
            enrollment = Enrollment.objects.get(student=request.user, course=course)
        except Enrollment.DoesNotExist:
            messages.error(request, 'Anda harus menyelesaikan kursus ini untuk memberikan ulasan.')
            return redirect('course_detail', slug=course_slug)
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.student = request.user
            review.course = course
            review.save()
            messages.success(request, 'Ulasan berhasil ditambahkan.')
            return redirect('course_detail', slug=course_slug)
    
    return redirect('course_detail', slug=course_slug)