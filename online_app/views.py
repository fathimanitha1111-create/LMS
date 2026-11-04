from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.http import JsonResponse
from .models import (
    UserProfile, Category, Course, Lesson, LessonProgress,
    Enrollment, Quiz, Question, QuizResult, Assignment,
    AssignmentSubmission, Certificate, ContactMessage
)
from .forms import (
    UserRegistrationForm, UserLoginForm, UserUpdateForm, UserProfileForm,
    CourseForm, LessonForm, QuizForm, QuestionForm, AssignmentForm,
    AssignmentSubmissionForm, ContactForm
)


def global_categories_processor(request):
    return {
        'nav_categories': Category.objects.all()[:6]
    }


# ==============================================================================
# Public Informational Views
# ==============================================================================

def home(request):
    popular_courses = Course.objects.filter(is_published=True).select_related('category', 'instructor', 'instructor__profile')[:6]
    categories = Category.objects.annotate(course_count=Count('courses')).order_by('-course_count')[:6]
    instructors = User.objects.filter(profile__role='instructor').select_related('profile')[:4]
    
    total_students = UserProfile.objects.filter(role='student').count() or 1200
    total_courses = Course.objects.filter(is_published=True).count() or 45
    total_instructors = UserProfile.objects.filter(role='instructor').count() or 18

    context = {
        'popular_courses': popular_courses,
        'categories': categories,
        'instructors': instructors,
        'total_students': total_students,
        'total_courses': total_courses,
        'total_instructors': total_instructors,
    }
    return render(request, 'online_app/home.html', context)


def about(request):
    instructors = User.objects.filter(profile__role='instructor').select_related('profile')[:4]
    return render(request, 'online_app/about.html', {'instructors': instructors})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been sent successfully. We will respond shortly.")
            return redirect('contact')
        else:
            messages.error(request, "Please fix the errors in the form.")
    else:
        form = ContactForm()
    return render(request, 'online_app/contact.html', {'form': form})


# ==============================================================================
# Course Browsing & Details
# ==============================================================================

def courses(request):
    course_list = Course.objects.filter(is_published=True).select_related('category', 'instructor', 'instructor__profile')
    
    # Category filter
    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        course_list = course_list.filter(category=selected_category)
        
    # Search filter
    q = request.GET.get('q', '').strip()
    if q:
        course_list = course_list.filter(
            Q(title__icontains=q) |
            Q(short_description__icontains=q) |
            Q(description__icontains=q) |
            Q(category__name__icontains=q)
        )
        
    # Level filter
    level = request.GET.get('level')
    if level and level != 'all':
        course_list = course_list.filter(level=level)
        
    # Price filter
    price_filter = request.GET.get('price')
    if price_filter == 'free':
        course_list = course_list.filter(price=0)
    elif price_filter == 'paid':
        course_list = course_list.filter(price__gt=0)

    categories_all = Category.objects.all()

    context = {
        'courses': course_list,
        'categories': categories_all,
        'selected_category': selected_category,
        'search_query': q,
        'selected_level': level,
        'selected_price': price_filter,
        'total_results': course_list.count(),
    }
    return render(request, 'online_app/courses.html', context)


def course_detail(request, slug):
    course = get_object_or_404(
        Course.objects.select_related('category', 'instructor', 'instructor__profile').prefetch_related('lessons', 'quizzes', 'assignments'),
        slug=slug,
        is_published=True
    )
    
    is_enrolled = False
    enrollment = None
    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        is_enrolled = enrollment is not None

    lessons = course.lessons.all().order_by('order')
    first_lesson = lessons.first()
    quizzes = course.quizzes.all()
    assignments = course.assignments.all()
    
    related_courses = Course.objects.filter(category=course.category, is_published=True).exclude(id=course.id)[:3]

    context = {
        'course': course,
        'lessons': lessons,
        'first_lesson': first_lesson,
        'quizzes': quizzes,
        'assignments': assignments,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
        'related_courses': related_courses,
    }
    return render(request, 'online_app/course_detail.html', context)


@login_required
def enroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    
    if created:
        messages.success(request, f"You have successfully enrolled in '{course.title}'!")
    else:
        messages.info(request, f"You are already enrolled in '{course.title}'.")
        
    first_lesson = course.lessons.first()
    if first_lesson:
        return redirect('lessons', course_slug=course.slug, lesson_id=first_lesson.id)
    return redirect('course_detail', slug=course.slug)


# ==============================================================================
# Authentication & Profiles
# ==============================================================================

def user_register(request):
    if request.user.is_authenticated:
        return redirect('student_dashboard')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            role = form.cleaned_data.get('role', 'student')
            user.profile.role = role
            user.profile.save()
            
            login(request, user)
            messages.success(request, f"Welcome to Online LMS, {user.first_name or user.username}! Your account has been created.")
            if role == 'instructor':
                return redirect('instructor_dashboard')
            return redirect('student_dashboard')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = UserRegistrationForm()
    return render(request, 'online_app/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        if request.user.profile.is_instructor():
            return redirect('instructor_dashboard')
        return redirect('student_dashboard')
        
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            if user.profile.is_instructor():
                return redirect('instructor_dashboard')
            return redirect('student_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'online_app/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please check the form for errors.")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'online_app/profile.html', context)


# ==============================================================================
# Student Features
# ==============================================================================

@login_required
def student_dashboard(request):
    user = request.user
    enrollments = Enrollment.objects.filter(user=user).select_related('course', 'course__category').order_by('-enrolled_at')
    
    total_enrolled = enrollments.count()
    completed_courses = enrollments.filter(completed=True).count()
    in_progress = total_enrolled - completed_courses
    certificates_count = Certificate.objects.filter(user=user).count()
    
    recent_quiz_results = QuizResult.objects.filter(user=user).select_related('quiz', 'quiz__course')[:5]
    recent_submissions = AssignmentSubmission.objects.filter(user=user).select_related('assignment', 'assignment__course')[:5]

    context = {
        'enrollments': enrollments,
        'total_enrolled': total_enrolled,
        'completed_courses': completed_courses,
        'in_progress': in_progress,
        'certificates_count': certificates_count,
        'recent_quiz_results': recent_quiz_results,
        'recent_submissions': recent_submissions,
    }
    return render(request, 'online_app/student_dashboard.html', context)


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course', 'course__category', 'course__instructor').order_by('-enrolled_at')
    return render(request, 'online_app/my_courses.html', {'enrollments': enrollments})


@login_required
def lessons_view(request, course_slug, lesson_id):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    is_enrolled = course.is_enrolled_by(request.user)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    
    if not is_enrolled and not lesson.is_preview:
        messages.warning(request, "Please enroll in this course to access full lessons.")
        return redirect('course_detail', slug=course.slug)

    all_lessons = list(course.lessons.all().order_by('order', 'id'))
    current_idx = -1
    for idx, l in enumerate(all_lessons):
        if l.id == lesson.id:
            current_idx = idx
            break

    prev_lesson = all_lessons[current_idx - 1] if current_idx > 0 else None
    next_lesson = all_lessons[current_idx + 1] if current_idx >= 0 and current_idx < len(all_lessons) - 1 else None

    completed_lesson_ids = set(
        LessonProgress.objects.filter(
            user=request.user,
            lesson__course=course,
            completed=True
        ).values_list('lesson_id', flat=True)
    )

    is_completed = lesson.id in completed_lesson_ids
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    progress_percentage = enrollment.get_progress_percentage() if enrollment else 0

    context = {
        'course': course,
        'lesson': lesson,
        'all_lessons': all_lessons,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'is_completed': is_completed,
        'completed_lesson_ids': completed_lesson_ids,
        'progress_percentage': progress_percentage,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'online_app/lessons.html', context)


@login_required
def toggle_lesson_progress(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.course
    
    progress, created = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
    if not created:
        progress.completed = not progress.completed
        progress.save()
    else:
        progress.completed = True
        progress.save()

    total_lessons = course.get_total_lessons()
    completed_lessons = LessonProgress.objects.filter(
        user=request.user,
        lesson__course=course,
        completed=True
    ).count()

    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    if enrollment:
        if completed_lessons >= total_lessons and total_lessons > 0:
            enrollment.completed = True
            enrollment.completed_at = timezone.now()
            enrollment.save()
            # Issue certificate automatically
            Certificate.objects.get_or_create(user=request.user, course=course)
        else:
            enrollment.completed = False
            enrollment.completed_at = None
            enrollment.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax'):
        percentage = enrollment.get_progress_percentage() if enrollment else 0
        return JsonResponse({
            'success': True,
            'completed': progress.completed,
            'progress_percentage': percentage,
            'all_completed': enrollment.completed if enrollment else False,
        })

    messages.success(request, "Lesson status updated!")
    return redirect('lessons', course_slug=course.slug, lesson_id=lesson.id)


@login_required
def quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz.objects.select_related('course'), id=quiz_id)
    questions = quiz.questions.all()
    user_result = QuizResult.objects.filter(user=request.user, quiz=quiz).first()
    
    submitted = False
    score = 0
    total = questions.count()
    percentage = 0
    passed = False

    if request.method == 'POST':
        score = 0
        for q in questions:
            selected_option = request.POST.get(f'question_{q.id}')
            if selected_option and int(selected_option) == q.correct_option:
                score += 1
                
        percentage = round((score / total) * 100, 1) if total > 0 else 0
        passed = percentage >= quiz.pass_mark
        
        user_result, _ = QuizResult.objects.update_or_create(
            user=request.user,
            quiz=quiz,
            defaults={
                'score': score,
                'total_marks': total,
                'percentage': percentage,
                'passed': passed,
            }
        )
        submitted = True
        messages.success(request, f"Quiz submitted! You scored {score}/{total} ({percentage}%).")

    context = {
        'quiz': quiz,
        'questions': questions,
        'user_result': user_result,
        'submitted': submitted,
        'score': score,
        'total': total,
        'percentage': percentage,
        'passed': passed,
    }
    return render(request, 'online_app/quiz.html', context)


@login_required
def assignments_view(request, assignment_id):
    assignment = get_object_or_404(Assignment.objects.select_related('course'), id=assignment_id)
    existing_submission = AssignmentSubmission.objects.filter(user=request.user, assignment=assignment).first()
    
    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES, instance=existing_submission)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.user = request.user
            sub.assignment = assignment
            sub.save()
            messages.success(request, "Your assignment solution has been submitted successfully!")
            return redirect('assignments', assignment_id=assignment.id)
        else:
            messages.error(request, "Please fix the submission errors.")
    else:
        form = AssignmentSubmissionForm(instance=existing_submission)

    context = {
        'assignment': assignment,
        'existing_submission': existing_submission,
        'form': form,
    }
    return render(request, 'online_app/assignments.html', context)


@login_required
def certificates_view(request):
    certificates = Certificate.objects.filter(user=request.user).select_related('course', 'course__instructor')
    
    # Check if a specific certificate is requested for viewing
    cert_code = request.GET.get('code')
    active_cert = None
    if cert_code:
        active_cert = get_object_or_404(Certificate.objects.select_related('course', 'user'), certificate_code=cert_code)

    context = {
        'certificates': certificates,
        'active_cert': active_cert,
    }
    return render(request, 'online_app/certificates.html', context)


# ==============================================================================
# Instructor Features & CRUD
# ==============================================================================

@login_required
def instructor_dashboard(request):
    if not request.user.profile.is_instructor():
        messages.warning(request, "Access restricted to instructors.")
        return redirect('student_dashboard')

    courses_taught = Course.objects.filter(instructor=request.user).prefetch_related('enrollments', 'lessons', 'quizzes', 'assignments')
    total_courses = courses_taught.count()
    total_students = Enrollment.objects.filter(course__instructor=request.user).count()
    
    recent_enrollments = Enrollment.objects.filter(course__instructor=request.user).select_related('user', 'course').order_by('-enrolled_at')[:8]

    context = {
        'courses': courses_taught,
        'total_courses': total_courses,
        'total_students': total_students,
        'recent_enrollments': recent_enrollments,
    }
    return render(request, 'online_app/instructor_dashboard.html', context)


@login_required
def create_course(request):
    if not request.user.profile.is_instructor():
        messages.error(request, "Permission denied.")
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, f"Course '{course.title}' created successfully! Now you can add lessons.")
            return redirect('instructor_dashboard')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = CourseForm()
    return render(request, 'online_app/course_form.html', {'form': form, 'action': 'Create Course'})


@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f"Course '{course.title}' updated successfully!")
            return redirect('instructor_dashboard')
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = CourseForm(instance=course)
    return render(request, 'online_app/course_form.html', {'form': form, 'action': f"Edit Course: {course.title}", 'course': course})


@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        title = course.title
        course.delete()
        messages.success(request, f"Course '{title}' was deleted successfully.")
        return redirect('instructor_dashboard')
    return render(request, 'online_app/course_confirm_delete.html', {'course': course})


@login_required
def add_lesson(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, f"Lesson '{lesson.title}' added to course.")
            return redirect('course_detail', slug=course.slug)
    else:
        form = LessonForm(initial={'order': course.get_total_lessons() + 1})
    return render(request, 'online_app/lesson_form.html', {'form': form, 'course': course})


@login_required
def add_quiz(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            messages.success(request, f"Quiz '{quiz.title}' created! Now add questions.")
            return redirect('add_question', quiz_id=quiz.id)
    else:
        form = QuizForm()
    return render(request, 'online_app/quiz_form.html', {'form': form, 'course': course})


@login_required
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, course__instructor=request.user)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.quiz = quiz
            q.save()
            messages.success(request, "Question added! Add another question or finish.")
            if 'save_and_add' in request.POST:
                return redirect('add_question', quiz_id=quiz.id)
            return redirect('course_detail', slug=quiz.course.slug)
    else:
        form = QuestionForm()
    return render(request, 'online_app/question_form.html', {'form': form, 'quiz': quiz})


@login_required
def add_assignment(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            messages.success(request, f"Assignment '{assignment.title}' created.")
            return redirect('course_detail', slug=course.slug)
    else:
        form = AssignmentForm()
    return render(request, 'online_app/assignment_form.html', {'form': form, 'course': course})
