from django import forms
from .models import Course, Module, Lesson


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'difficulty', 'price', 'duration', 'thumbnail', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mengatur label untuk field-field
        self.fields['title'].label = 'Judul Kursus'
        self.fields['description'].label = 'Deskripsi'
        self.fields['category'].label = 'Kategori'
        self.fields['difficulty'].label = 'Tingkat Kesulitan'
        self.fields['price'].label = 'Harga'
        self.fields['duration'].label = 'Durasi (jam)'
        self.fields['thumbnail'].label = 'Thumbnail'
        self.fields['is_published'].label = 'Publikasikan Kursus'


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mengatur label untuk field-field
        self.fields['title'].label = 'Judul Modul'
        self.fields['description'].label = 'Deskripsi'
        self.fields['order'].label = 'Urutan'


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'lesson_type', 'video_url', 'duration', 'order', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'lesson_type': forms.Select(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mengatur label untuk field-field
        self.fields['title'].label = 'Judul Pelajaran'
        self.fields['content'].label = 'Konten'
        self.fields['lesson_type'].label = 'Jenis Pelajaran'
        self.fields['video_url'].label = 'URL Video (opsional)'
        self.fields['duration'].label = 'Durasi (menit)'
        self.fields['order'].label = 'Urutan'
        self.fields['is_published'].label = 'Publikasikan Pelajaran'