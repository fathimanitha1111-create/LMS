from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from online_app.models import (
    UserProfile, Category, Course, Lesson, LessonProgress,
    Enrollment, Quiz, Question, QuizResult, Assignment,
    AssignmentSubmission, Certificate
)


class OnlineLMSTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Student user
        self.student_user = User.objects.create_user(
            username='test_student',
            email='student@example.com',
            password='Password123!'
        )
        self.student_user.profile.role = 'student'
        self.student_user.profile.save()

        # Instructor user
        self.instructor_user = User.objects.create_user(
            username='test_instructor',
            email='instructor@example.com',
            password='Password123!',
            is_staff=True
        )
        self.instructor_user.profile.role = 'instructor'
        self.instructor_user.profile.save()

        # Category
        self.category = Category.objects.create(name='Web Development', slug='web-dev')

        # Course
        self.course = Course.objects.create(
            title='Intro to Django Web Development',
            slug='intro-django-web-dev',
            category=self.category,
            instructor=self.instructor_user,
            short_description='Learn Django from scratch',
            description='In-depth course on Django',
            price=0.00,
            level='beginner',
            is_published=True
        )

        # Lesson
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Lesson 1: Introduction',
            order=1,
            content='Welcome to the course notes.',
            duration_minutes=15,
            is_preview=True
        )

        # Quiz & Question
        self.quiz = Quiz.objects.create(course=self.course, title='Django Basics Quiz', pass_mark=50)
        self.question = Question.objects.create(
            quiz=self.quiz,
            question_text='What is Django?',
            option1='A web framework',
            option2='A database',
            option3='An OS',
            option4='A compiler',
            correct_option=1,
            explanation='Django is a high-level Python web framework.'
        )

        # Assignment
        self.assignment = Assignment.objects.create(
            course=self.course,
            title='Project 1: Setup',
            description='Initialize a project',
            max_marks=100
        )

    def test_public_pages_load(self):
        for route_name in ['home', 'about', 'contact', 'courses', 'login', 'register']:
            response = self.client.get(reverse(route_name))
            self.assertEqual(response.status_code, 200, f"Route {route_name} failed with {response.status_code}")

    def test_course_detail_page(self):
        response = self.client.get(reverse('course_detail', kwargs={'slug': self.course.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.course.title)

    def test_student_enrollment_and_lesson(self):
        self.client.login(username='test_student', password='Password123!')
        
        # Enroll
        enroll_url = reverse('enroll_course', kwargs={'slug': self.course.slug})
        response = self.client.get(enroll_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Enrollment.objects.filter(user=self.student_user, course=self.course).exists())

        # View lesson
        lesson_url = reverse('lessons', kwargs={'course_slug': self.course.slug, 'lesson_id': self.lesson.id})
        response = self.client.get(lesson_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lesson 1: Introduction')

        # Toggle lesson completion
        toggle_url = reverse('toggle_lesson_progress', kwargs={'lesson_id': self.lesson.id})
        toggle_response = self.client.get(toggle_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(toggle_response.status_code, 200)
        json_data = toggle_response.json()
        self.assertTrue(json_data['completed'])
        self.assertTrue(LessonProgress.objects.filter(user=self.student_user, lesson=self.lesson, completed=True).exists())

    def test_quiz_submission_and_scoring(self):
        self.client.login(username='test_student', password='Password123!')
        quiz_url = reverse('quiz', kwargs={'quiz_id': self.quiz.id})
        
        # Submit correct option 1
        post_data = {f'question_{self.question.id}': '1'}
        response = self.client.post(quiz_url, data=post_data)
        self.assertEqual(response.status_code, 200)
        
        result = QuizResult.objects.filter(user=self.student_user, quiz=self.quiz).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.score, 1)
        self.assertTrue(result.passed)

    def test_assignment_submission(self):
        self.client.login(username='test_student', password='Password123!')
        assign_url = reverse('assignments', kwargs={'assignment_id': self.assignment.id})
        
        post_data = {'submission_text': 'Here is my completed assignment solution.'}
        response = self.client.post(assign_url, data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(AssignmentSubmission.objects.filter(user=self.student_user, assignment=self.assignment).exists())

    def test_instructor_course_crud(self):
        self.client.login(username='test_instructor', password='Password123!')
        
        # 1. Dashboard
        response = self.client.get(reverse('instructor_dashboard'))
        self.assertEqual(response.status_code, 200)

        # 2. Create Course
        create_url = reverse('create_course')
        post_data = {
            'title': 'New Test Course By Instructor',
            'category': self.category.id,
            'short_description': 'A new test course description',
            'description': 'Full detailed syllabus description',
            'price': '19.99',
            'level': 'intermediate',
            'duration_hours': '8.0',
            'is_published': True
        }
        res = self.client.post(create_url, data=post_data, follow=True)
        self.assertEqual(res.status_code, 200)
        new_course = Course.objects.filter(title='New Test Course By Instructor').first()
        self.assertIsNotNone(new_course)

        # 3. Edit Course
        edit_url = reverse('edit_course', kwargs={'course_id': new_course.id})
        post_data['title'] = 'Updated Test Course Title'
        res_edit = self.client.post(edit_url, data=post_data, follow=True)
        self.assertEqual(res_edit.status_code, 200)
        new_course.refresh_from_db()
        self.assertEqual(new_course.title, 'Updated Test Course Title')

        # 4. Delete Course
        delete_url = reverse('delete_course', kwargs={'course_id': new_course.id})
        res_del = self.client.post(delete_url, follow=True)
        self.assertEqual(res_del.status_code, 200)
        self.assertFalse(Course.objects.filter(id=new_course.id).exists())
