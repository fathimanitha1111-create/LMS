from django.urls import path
from . import views

urlpatterns = [
    # Public & Informational
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Courses
    path('courses/', views.courses, name='courses'),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('course/<slug:slug>/enroll/', views.enroll_course, name='enroll_course'),
    
    # Learning, Quizzes & Assignments
    path('course/<slug:course_slug>/learn/<int:lesson_id>/', views.lessons_view, name='lessons'),
    path('lesson/<int:lesson_id>/toggle/', views.toggle_lesson_progress, name='toggle_lesson_progress'),
    path('quiz/<int:quiz_id>/', views.quiz_view, name='quiz'),
    path('assignment/<int:assignment_id>/', views.assignments_view, name='assignments'),
    path('certificates/', views.certificates_view, name='certificates'),
    
    # Auth & Profile
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # Dashboards
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('instructor/dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    
    # Instructor Actions
    path('instructor/course/add/', views.create_course, name='create_course'),
    path('instructor/course/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('instructor/course/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('instructor/course/<int:course_id>/lesson/add/', views.add_lesson, name='add_lesson'),
    path('instructor/course/<int:course_id>/quiz/add/', views.add_quiz, name='add_quiz'),
    path('instructor/quiz/<int:quiz_id>/question/add/', views.add_question, name='add_question'),
    path('instructor/course/<int:course_id>/assignment/add/', views.add_assignment, name='add_assignment'),
]
