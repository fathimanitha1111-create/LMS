import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.templatetags.static import static


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=25, blank=True)
    headline = models.CharField(max_length=150, blank=True, help_text="e.g. Senior Software Engineer | Student")
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    avatar_static = models.CharField(max_length=255, blank=True, default='online_app/images/instructors/instructor1.jpg')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    def is_instructor(self):
        return self.role in ['instructor', 'admin'] or self.user.is_staff

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        if self.avatar_static:
            return static(self.avatar_static)
        return static('online_app/images/instructors/instructor1.jpg')


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=60, default='bi-code-slash', help_text="Bootstrap icon class name")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    image_static = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_course_count(self):
        return self.courses.filter(is_published=True).count()

    def get_image_url(self):
        if self.image:
            return self.image.url
        if self.image_static:
            return static(self.image_static)
        category_map = {
            'python-programming': 'online_app/images/categories/python.jpg',
            'web-development': 'online_app/images/categories/web_dev.jpg',
            'data-science-ai': 'online_app/images/categories/data_science.jpg',
            'frontend-engineering': 'online_app/images/categories/web_dev.jpg',
            'ui-ux-design': 'online_app/images/categories/ui_ux.jpg',
            'mobile-development': 'online_app/images/categories/mobile_dev.jpg',
            'cloud-computing': 'online_app/images/categories/cloud_computing.jpg',
            'cloud-devops': 'online_app/images/categories/cloud_computing.jpg',
            'artificial-intelligence': 'online_app/images/categories/ai.jpg',
            'digital-marketing': 'online_app/images/categories/digital_marketing.jpg',
        }
        return static(category_map.get(self.slug, 'online_app/images/categories/web_dev.jpg'))


class Course(models.Model):
    LEVEL_CHOICES = [
        ('all', 'All Levels'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_created')
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='all')
    thumbnail = models.ImageField(upload_to='courses/', blank=True, null=True)
    thumbnail_static = models.CharField(max_length=255, blank=True, default='online_app/images/courses/course1.png')
    duration_hours = models.DecimalField(max_digits=5, decimal_places=1, default=10.0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or 'course'
            slug = base_slug
            counter = 1
            while Course.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        if self.thumbnail_static:
            return static(self.thumbnail_static)
        course_map = {
            'python-django-fullstack-bootcamp': 'online_app/images/courses/python.jpg',
            'machine-learning-ai-python': 'online_app/images/courses/ai.jpg',
            'responsive-web-design-bootstrap-5': 'online_app/images/courses/web_dev.jpg',
            'cloud-devops-docker-kubernetes': 'online_app/images/courses/cloud_computing.jpg',
            'ui-ux-design-systems-figma': 'online_app/images/courses/ui_ux.jpg',
            'cross-platform-mobile-apps-flutter': 'online_app/images/courses/mobile_dev.jpg',
            'data-science-analytics-python': 'online_app/images/courses/data_science.jpg',
            'digital-marketing-growth-analytics': 'online_app/images/courses/digital_marketing.jpg',
        }
        return static(course_map.get(self.slug, 'online_app/images/courses/python.jpg'))

    def is_free(self):
        return self.price == 0

    def get_total_lessons(self):
        return self.lessons.count()

    def get_total_students(self):
        return self.enrollments.count()

    def is_enrolled_by(self, user):
        if not user.is_authenticated:
            return False
        return self.enrollments.filter(user=user).exists()


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'course')
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.user.username} -> {self.course.title}"

    def get_progress_percentage(self):
        total_lessons = self.course.get_total_lessons()
        if total_lessons == 0:
            return 100 if self.completed else 0
        completed_lessons = LessonProgress.objects.filter(
            user=self.user,
            lesson__course=self.course,
            completed=True
        ).count()
        return min(100, int((completed_lessons / total_lessons) * 100))

    def get_completed_lessons_count(self):
        return LessonProgress.objects.filter(
            user=self.user,
            lesson__course=self.course,
            completed=True
        ).count()


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=1)
    content = models.TextField(blank=True, help_text="Lesson reading notes and material")
    video_url = models.CharField(max_length=300, blank=True, help_text="YouTube or video embed URL")
    pdf_file = models.FileField(upload_to='study_materials/', blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(default=15)
    is_preview = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.course.title} - Lesson {self.order}: {self.title}"

    def is_completed_by(self, user):
        if not user.is_authenticated:
            return False
        return LessonProgress.objects.filter(user=user, lesson=self, completed=True).exists()


class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    completed = models.BooleanField(default=True)
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} ({'Done' if self.completed else 'Pending'})"


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pass_mark = models.PositiveIntegerField(default=60, help_text="Pass percentage (e.g. 60)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - Quiz: {self.title}"

    def get_questions_count(self):
        return self.questions.count()


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.PositiveSmallIntegerField(
        choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')],
        default=1
    )
    explanation = models.TextField(blank=True)

    def __str__(self):
        return f"Q: {self.question_text[:50]}"


class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    score = models.PositiveIntegerField(default=0)
    total_marks = models.PositiveIntegerField(default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    passed = models.BooleanField(default=False)
    date_taken = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_taken']

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score}/{self.total_marks})"


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField(null=True, blank=True)
    max_marks = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - Assignment: {self.title}"


class AssignmentSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    submission_text = models.TextField(blank=True)
    submission_file = models.FileField(upload_to='assignments/', blank=True, null=True)
    marks_awarded = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'assignment')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.user.username} submission for {self.assignment.title}"


class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    certificate_code = models.CharField(max_length=50, unique=True)
    issued_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
        ordering = ['-issued_date']

    def save(self, *args, **kwargs):
        if not self.certificate_code:
            self.certificate_code = f"CERT-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Certificate {self.certificate_code} for {self.user.username} ({self.course.title})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name}: {self.subject}"
