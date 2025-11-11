from django.core.management.base import BaseCommand
from courses.models import HomePageHero, HomePageFeature, HomePageFloatingCard, Instructor, HomePageCTA
from users.models import User


class Command(BaseCommand):
    help = 'Create initial data for home page models'

    def handle(self, *args, **options):
        # Create HomePageHero instance
        hero, created = HomePageHero.objects.get_or_create(
            id=1,
            defaults={
                'title': 'Transform Your Future with Expert-Led Online Courses',
                'subtitle': 'Discover thousands of high-quality courses designed by industry professionals. Learn at your own pace, gain in-demand skills, and advance your career from anywhere in the world.',
                'students_count': 50000,
                'courses_count': 1200,
                'success_rate': 98,
                'feature_1_title': 'Certified Programs',
                'feature_2_title': 'Lifetime Access',
                'feature_3_title': 'Expert Instructors',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created HomePageHero'))

        # Create HomePageFeatures
        features_data = [
            {
                'icon_class': 'fas fa-laptop-code',
                'title': 'Belajar Online',
                'description': 'Akses kursus kapanpun dan dimanapun sesuai dengan jadwal Anda.',
                'order': 1
            },
            {
                'icon_class': 'fas fa-certificate',
                'title': 'Sertifikat',
                'description': 'Dapatkan sertifikat setelah menyelesaikan kursus untuk meningkatkan CV Anda.',
                'order': 2
            },
            {
                'icon_class': 'fas fa-user-tie',
                'title': 'Instruktur Profesional',
                'description': 'Berlatih dengan instruktur berpengalaman di bidangnya.',
                'order': 3
            }
        ]
        
        for feature_data in features_data:
            feature, created = HomePageFeature.objects.get_or_create(
                title=feature_data['title'],
                defaults=feature_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created HomePageFeature: {feature.title}'))

        # Create HomePageFloatingCards
        floating_cards_data = [
            {
                'icon_class': 'bi bi-code-slash',
                'title': 'Web Development',
                'student_count': 2450,
                'order': 1
            },
            {
                'icon_class': 'bi bi-palette',
                'title': 'UI/UX Design',
                'student_count': 1890,
                'order': 2
            },
            {
                'icon_class': 'bi bi-graph-up',
                'title': 'Digital Marketing',
                'student_count': 3200,
                'order': 3
            }
        ]
        
        for card_data in floating_cards_data:
            card, created = HomePageFloatingCard.objects.get_or_create(
                title=card_data['title'],
                defaults=card_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created HomePageFloatingCard: {card.title}'))

        # Create Instructors
        instructors_data = [
            {
                'name': 'Sarah Johnson',
                'specialty': 'Web Development',
                'description': 'Nulla facilisi morbi tempus iaculis urna id volutpat lacus laoreet non curabitur gravida.',
                'rating': 4.8,
                'course_count': 18,
                'student_count': 2100,
                'linkedin_url': 'https://linkedin.com/in/sarahjohnson',
                'twitter_url': 'https://twitter.com/sarahjohnson',
                'order': 1
            },
            {
                'name': 'Michael Chen',
                'specialty': 'Data Science',
                'description': 'Suspendisse potenti nullam ac tortor vitae purus faucibus ornare suspendisse sed nisi.',
                'rating': 4.9,
                'course_count': 24,
                'student_count': 3500,
                'github_url': 'https://github.com/michaelchen',
                'linkedin_url': 'https://linkedin.com/in/michaelchen',
                'order': 2
            },
            {
                'name': 'Amanda Rodriguez',
                'specialty': 'UX Design',
                'description': 'Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis.',
                'rating': 4.6,
                'course_count': 15,
                'student_count': 1800,
                'dribbble_url': 'https://dribbble.com/amandarodriguez',
                'behance_url': 'https://behance.com/amandarodriguez',
                'order': 3
            },
            {
                'name': 'David Thompson',
                'specialty': 'Digital Marketing',
                'description': 'Vivamus magna justo lacinia eget consectetur sed convallis at tellus curabitur non nulla.',
                'rating': 4.7,
                'course_count': 21,
                'student_count': 2900,
                'instagram_url': 'https://instagram.com/davidthompson',
                'facebook_url': 'https://facebook.com/davidthompson',
                'order': 4
            }
        ]
        
        for instructor_data in instructors_data:
            instructor, created = Instructor.objects.get_or_create(
                name=instructor_data['name'],
                defaults=instructor_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created Instructor: {instructor.name}'))

        # Create HomePageCTA
        cta, created = HomePageCTA.objects.get_or_create(
            id=1,
            defaults={
                'title': 'Transform Your Future with Expert-Led Online Courses',
                'subtitle': 'Join thousands of successful learners who have advanced their careers through our comprehensive online education platform.',
                'feature_1': '20+ Expert instructors with industry experience',
                'feature_2': 'Certificate of completion for every course',
                'feature_3': '24/7 access to course materials and resources',
                'feature_4': 'Interactive assignments and real-world projects',
                'cta_students_count': 15000,
                'cta_courses_count': 150,
                'cta_success_rate': 98,
                'cta_button_text': 'Browse Courses',
                'cta_button_url': '#courses',
                'secondary_button_text': 'Enroll Now',
                'secondary_button_url': '#enroll',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created HomePageCTA'))

        self.stdout.write(self.style.SUCCESS('Successfully created initial home page data'))