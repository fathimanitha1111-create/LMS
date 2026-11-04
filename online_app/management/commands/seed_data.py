from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from online_app.models import (
    UserProfile, Category, Course, Lesson, LessonProgress,
    Enrollment, Quiz, Question, QuizResult, Assignment,
    AssignmentSubmission, Certificate, ContactMessage
)


class Command(BaseCommand):
    help = 'Seeds database with realistic demo courses, instructors, students, quizzes, and lessons with local image assets.'

    def handle(self, *args, **options):
        self.stdout.write("Starting database seed with local educational images...")

        # 1. Admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@eduvibe-lms.edu',
                'first_name': 'EduVibe',
                'last_name': 'Administrator',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
        admin_user.profile.role = 'admin'
        admin_user.profile.headline = 'Head Academic Administrator'
        admin_user.profile.avatar_static = 'online_app/images/instructors/instructor1.jpg'
        admin_user.profile.save()

        # 2. Instructors
        instructor1, created = User.objects.get_or_create(
            username='instructor_john',
            defaults={
                'email': 'john.doe@eduvibe-lms.edu',
                'first_name': 'John',
                'last_name': 'Doe',
                'is_staff': True,
            }
        )
        if created:
            instructor1.set_password('password123')
            instructor1.save()
        instructor1.profile.role = 'instructor'
        instructor1.profile.headline = 'Principal Python & Django Architect'
        instructor1.profile.bio = '12+ years building resilient web infrastructure and mentoring software engineers.'
        instructor1.profile.avatar_static = 'online_app/images/instructors/instructor1.jpg'
        instructor1.profile.save()

        instructor2, created = User.objects.get_or_create(
            username='sarah_jenkins',
            defaults={
                'email': 'sarah.jenkins@eduvibe-lms.edu',
                'first_name': 'Sarah',
                'last_name': 'Jenkins',
                'is_staff': True,
            }
        )
        if created:
            instructor2.set_password('password123')
            instructor2.save()
        instructor2.profile.role = 'instructor'
        instructor2.profile.headline = 'AI Engineer & Deep Learning Researcher'
        instructor2.profile.bio = 'Stanford CS graduate focused on pragmatic machine learning models and neural networks.'
        instructor2.profile.avatar_static = 'online_app/images/instructors/instructor2.jpg'
        instructor2.profile.save()

        instructor3, created = User.objects.get_or_create(
            username='david_miller',
            defaults={
                'email': 'david.miller@eduvibe-lms.edu',
                'first_name': 'David',
                'last_name': 'Miller',
                'is_staff': True,
            }
        )
        if created:
            instructor3.set_password('password123')
            instructor3.save()
        instructor3.profile.role = 'instructor'
        instructor3.profile.headline = 'Cloud & DevOps Architect'
        instructor3.profile.bio = 'Specialized in microservices, Kubernetes, and enterprise automated CI/CD pipelines.'
        instructor3.profile.avatar_static = 'online_app/images/instructors/instructor3.jpg'
        instructor3.profile.save()

        instructor4, created = User.objects.get_or_create(
            username='emily_watson',
            defaults={
                'email': 'emily.watson@eduvibe-lms.edu',
                'first_name': 'Emily',
                'last_name': 'Watson',
                'is_staff': True,
            }
        )
        if created:
            instructor4.set_password('password123')
            instructor4.save()
        instructor4.profile.role = 'instructor'
        instructor4.profile.headline = 'Design Director & UI/UX Specialist'
        instructor4.profile.bio = '10+ years designing digital product experiences and scalable design systems.'
        instructor4.profile.avatar_static = 'online_app/images/instructors/instructor4.jpg'
        instructor4.profile.save()

        # 3. Student Demo
        student, created = User.objects.get_or_create(
            username='student_alex',
            defaults={
                'email': 'alex.rivera@example.com',
                'first_name': 'Alex',
                'last_name': 'Rivera',
            }
        )
        if created:
            student.set_password('password123')
            student.save()
        student.profile.role = 'student'
        student.profile.headline = 'Aspiring Full-Stack Software Engineer'
        student.profile.avatar_static = 'online_app/images/instructors/instructor3.jpg'
        student.profile.save()

        # 4. Categories (8 Topics)
        categories_data = [
            ('Python Programming', 'python-programming', 'bi-code-square', 'Python, OOP, automation, and backend development.', 'online_app/images/categories/python.jpg'),
            ('Web Development', 'web-development', 'bi-code-slash', 'Python, Django, HTML5, CSS3, JavaScript, and Bootstrap 5.', 'online_app/images/categories/web_dev.jpg'),
            ('Data Science', 'data-science', 'bi-bar-chart-line-fill', 'Machine Learning, Pandas, NumPy, and statistical analysis.', 'online_app/images/categories/data_science.jpg'),
            ('UI/UX Design', 'ui-ux-design', 'bi-brush-fill', 'Modern Figma design systems, wireframing, and user research.', 'online_app/images/categories/ui_ux.jpg'),
            ('Mobile Development', 'mobile-development', 'bi-phone-fill', 'Cross-platform iOS and Android apps with Flutter.', 'online_app/images/categories/mobile_dev.jpg'),
            ('Cloud Computing', 'cloud-computing', 'bi-cloud-check-fill', 'Docker, Kubernetes, AWS, and modern DevOps architecture.', 'online_app/images/categories/cloud_computing.jpg'),
            ('Artificial Intelligence', 'artificial-intelligence', 'bi-cpu-fill', 'Deep Learning, Neural Networks, PyTorch, and LLMs.', 'online_app/images/categories/ai.jpg'),
            ('Digital Marketing', 'digital-marketing', 'bi-megaphone-fill', 'Growth analytics, SEO strategies, Google Ads, and conversions.', 'online_app/images/categories/digital_marketing.jpg'),
        ]

        category_objs = {}
        for name, slug, icon, desc, img_path in categories_data:
            cat, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'icon': icon, 'description': desc, 'image_static': img_path}
            )
            cat.name = name
            cat.icon = icon
            cat.description = desc
            cat.image_static = img_path
            cat.save()
            category_objs[slug] = cat

        # 5. Courses (8 Educational Topics with Local Thumbnails)
        courses_data = [
            {
                'title': 'Python Django: The Complete Full-Stack Web Development Bootcamp',
                'slug': 'python-django-fullstack-bootcamp',
                'category': category_objs['web-development'],
                'instructor': instructor1,
                'short_description': 'Build production-ready, responsive web applications from scratch with Python, Django 5, Bootstrap 5, and SQLite.',
                'description': """Welcome to the most complete, project-oriented Python Django masterclass available.

In this course, you will learn the core foundations of the Django framework, including:
- MTV (Model-Template-View) design patterns
- Relational schema modeling and migrations with SQLite
- Bootstrap 5 responsive layout and mobile-first design
- User Authentication, roles, and session security
- Asynchronous lesson progress and interactive quizzes

You will finish this course having built fully working real-world applications for your portfolio.""",
                'price': 49.99,
                'level': 'beginner',
                'duration_hours': 14.5,
                'thumbnail_static': 'online_app/images/courses/python.jpg',
                'lessons': [
                    ('Welcome & Environment Setup', 'https://www.youtube.com/embed/rfscVS0vtbw', 15, True, 'In this lesson, we initialize Python 3, create virtual environments, and explore manage.py.'),
                    ('Django Models & SQLite ORM', 'https://www.youtube.com/embed/F5mRW0jo-U4', 22, False, 'Explore ForeignKeys, OneToOne relationships, database migrations, and queries.'),
                    ('Bootstrap 5 Responsive Grid & Layouts', 'https://www.youtube.com/embed/-qfEOE4vtxE', 25, False, 'Integrate Bootstrap 5 breakpoints, containers, cards, and offcanvas navigation.'),
                    ('Authentication & Role-Based Access', 'https://www.youtube.com/embed/rHux0gMZ3Eg', 20, False, 'Implement secure student and instructor registration, login, and dashboard routing.'),
                ],
                'quiz': {
                    'title': 'Django Fundamentals Quiz',
                    'pass_mark': 60,
                    'questions': [
                        ('What architecture pattern does Django follow?', 'MVC / MTV (Model Template View)', 'MVP', 'Monolithic Single File', 'Flux', 1, 'Django uses the Model-Template-View architectural pattern.'),
                        ('Which file is used to define database models in a Django app?', 'views.py', 'models.py', 'urls.py', 'settings.py', 2, 'Models are declared in models.py.'),
                        ('What command creates new database migration files?', 'python manage.py runserver', 'python manage.py makemigrations', 'python manage.py test', 'python manage.py check', 2, 'makemigrations packages model changes into migration scripts.')
                    ]
                },
                'assignment': {
                    'title': 'Build a Portfolio Model & View',
                    'description': 'Create a custom Django Model with at least 4 fields, write a migration, and create a responsive Bootstrap template rendering items from the database.',
                    'max_marks': 100
                }
            },
            {
                'title': 'Full-Stack Web Development with HTML5, CSS3, JavaScript & Bootstrap',
                'slug': 'fullstack-web-development-html-css-js',
                'category': category_objs['web-development'],
                'instructor': instructor1,
                'short_description': 'Master frontend styling, interactive JavaScript ES6, and responsive Bootstrap 5 components for modern web applications.',
                'description': 'Learn to design beautiful, accessible, mobile-first web pages with CSS Grid, Flexbox, JavaScript DOM manipulation, and responsive UI cards.',
                'price': 29.99,
                'level': 'all',
                'duration_hours': 10.0,
                'thumbnail_static': 'online_app/images/courses/web_dev.jpg',
                'lessons': [
                    ('Semantic HTML5 & Modern CSS3 Layouts', 'https://www.youtube.com/embed/-qfEOE4vtxE', 18, True, 'Master responsive row-col classes across mobile, tablet, and desktop screens.'),
                ],
                'quiz': None,
                'assignment': None
            },
            {
                'title': 'Data Science & Analytics with Python & Pandas',
                'slug': 'data-science-analytics-python',
                'category': category_objs['data-science'],
                'instructor': instructor2,
                'short_description': 'Perform data wrangling, exploratory analysis, and visualization using Pandas, NumPy, Matplotlib, and Seaborn.',
                'description': 'Learn to inspect datasets, clean corrupted data, calculate statistical distributions, and build high-impact analytical charts.',
                'price': 0.00,
                'level': 'beginner',
                'duration_hours': 12.0,
                'thumbnail_static': 'online_app/images/courses/data_science.jpg',
                'lessons': [
                    ('Data Wrangling with Pandas & NumPy', 'https://www.youtube.com/embed/vmEHCJofslg', 20, True, 'Understand DataFrames, array manipulation, and cleaning datasets.'),
                ],
                'quiz': None,
                'assignment': None
            },
            {
                'title': 'Deep Learning & Artificial Intelligence with PyTorch',
                'slug': 'deep-learning-artificial-intelligence',
                'category': category_objs['artificial-intelligence'],
                'instructor': instructor2,
                'short_description': 'Build convolutional neural networks, transformer models, and AI pipelines with PyTorch and Python.',
                'description': 'Comprehensive foundation in modern AI architectures, backpropagation, tensor operations, computer vision, and NLP.',
                'price': 0.00,
                'level': 'intermediate',
                'duration_hours': 18.0,
                'thumbnail_static': 'online_app/images/courses/ai.jpg',
                'lessons': [
                    ('Tensors & Neural Network Foundations', 'https://www.youtube.com/embed/vmEHCJofslg', 20, True, 'Understand multidimensional tensors and loss functions.'),
                    ('Supervised Learning with PyTorch', 'https://www.youtube.com/embed/a9UrKTVEeZA', 25, False, 'Train classification pipelines on realistic data.'),
                ],
                'quiz': {
                    'title': 'Machine Learning Core Principles',
                    'pass_mark': 70,
                    'questions': [
                        ('Which library is standard for DataFrame manipulation in Python?', 'Requests', 'Pandas', 'Flask', 'Django', 2, 'Pandas is the primary library for data analysis and tabular manipulation.')
                    ]
                },
                'assignment': {
                    'title': 'Predictive Analysis Model',
                    'description': 'Train a decision tree classifier on a CSV dataset and submit the evaluation metrics (Accuracy, F1-Score).',
                    'max_marks': 100
                }
            },
            {
                'title': 'Modern UI/UX Design Systems in Figma: From Concept to Prototype',
                'slug': 'ui-ux-design-systems-figma',
                'category': category_objs['ui-ux-design'],
                'instructor': instructor4,
                'short_description': 'Design modern user interfaces, create interactive wireframes, and establish scalable design systems in Figma.',
                'description': 'Construct typography and color scales for accessibility, master auto-layout and components, and build interactive prototypes.',
                'price': 0.00,
                'level': 'beginner',
                'duration_hours': 8.0,
                'thumbnail_static': 'online_app/images/courses/ui_ux.jpg',
                'lessons': [
                    ('Figma Frames, Components & Auto-Layout', 'https://www.youtube.com/embed/c9Wg6Cb_YlU', 18, True, 'Create responsive UI components with auto-layout constraints.'),
                ],
                'quiz': None,
                'assignment': None
            },
            {
                'title': 'Cross-Platform Mobile Apps with Flutter & Dart',
                'slug': 'cross-platform-mobile-apps-flutter',
                'category': category_objs['mobile-development'],
                'instructor': instructor2,
                'short_description': 'Develop native iOS and Android apps with a single modern Flutter and Dart codebase.',
                'description': 'Write clean Dart code, build fluid widget trees, and manage application state with Riverpod and Bloc.',
                'price': 34.99,
                'level': 'intermediate',
                'duration_hours': 15.0,
                'thumbnail_static': 'online_app/images/courses/mobile_dev.jpg',
                'lessons': [
                    ('Flutter Widget Architecture & State', 'https://www.youtube.com/embed/1ukSR1GRtMU', 20, True, 'Understand Stateless vs Stateful widgets in Flutter.'),
                ],
                'quiz': None,
                'assignment': None
            },
            {
                'title': 'Cloud DevOps: Docker, Kubernetes & AWS Architecture',
                'slug': 'cloud-devops-docker-kubernetes-aws',
                'category': category_objs['cloud-computing'],
                'instructor': instructor3,
                'short_description': 'Containerize applications with Docker, orchestrate with Kubernetes, and automate deployments on AWS.',
                'description': 'Deep dive into microservices, containerization, Kubernetes pods, and automated GitHub Actions CI/CD pipelines.',
                'price': 39.99,
                'level': 'advanced',
                'duration_hours': 12.0,
                'thumbnail_static': 'online_app/images/courses/cloud_computing.jpg',
                'lessons': [
                    ('Introduction to Docker & Containers', 'https://www.youtube.com/embed/fqMOX6JJhGo', 22, True, 'Write Dockerfiles and launch multi-container stacks with Docker Compose.'),
                ],
                'quiz': None,
                'assignment': None
            },
            {
                'title': 'Digital Marketing Strategy, SEO & Growth Analytics',
                'slug': 'digital-marketing-growth-analytics',
                'category': category_objs['digital-marketing'],
                'instructor': instructor4,
                'short_description': 'Master search engine optimization (SEO), performance marketing, conversion funnels, and analytics.',
                'description': 'Learn how to drive targeted user acquisition, run profitable campaigns, and measure customer lifetime value.',
                'price': 24.99,
                'level': 'all',
                'duration_hours': 8.5,
                'thumbnail_static': 'online_app/images/courses/digital_marketing.jpg',
                'lessons': [
                    ('SEO Fundamentals & On-Page Optimization', 'https://www.youtube.com/embed/1ukSR1GRtMU', 20, True, 'Learn keyword research, meta architecture, and technical SEO audits.'),
                ],
                'quiz': None,
                'assignment': None
            }
        ]

        created_courses = []
        for cdata in courses_data:
            course, _ = Course.objects.get_or_create(
                slug=cdata['slug'],
                defaults={
                    'title': cdata['title'],
                    'category': cdata['category'],
                    'instructor': cdata['instructor'],
                    'short_description': cdata['short_description'],
                    'description': cdata['description'],
                    'price': cdata['price'],
                    'level': cdata['level'],
                    'duration_hours': cdata['duration_hours'],
                    'thumbnail_static': cdata['thumbnail_static'],
                    'is_published': True,
                }
            )
            course.title = cdata['title']
            course.category = cdata['category']
            course.instructor = cdata['instructor']
            course.short_description = cdata['short_description']
            course.description = cdata['description']
            course.price = cdata['price']
            course.level = cdata['level']
            course.duration_hours = cdata['duration_hours']
            course.thumbnail_static = cdata['thumbnail_static']
            course.is_published = True
            course.save()
            created_courses.append(course)

            # Lessons
            for idx, (ltitle, lvideo, ldur, lprev, lcontent) in enumerate(cdata['lessons'], start=1):
                Lesson.objects.get_or_create(
                    course=course,
                    order=idx,
                    defaults={
                        'title': ltitle,
                        'video_url': lvideo,
                        'duration_minutes': ldur,
                        'is_preview': lprev,
                        'content': lcontent,
                    }
                )

            # Quiz
            if cdata.get('quiz'):
                qdata = cdata['quiz']
                quiz, _ = Quiz.objects.get_or_create(
                    course=course,
                    title=qdata['title'],
                    defaults={'pass_mark': qdata['pass_mark']}
                )
                for qtext, o1, o2, o3, o4, cor, exp in qdata['questions']:
                    Question.objects.get_or_create(
                        quiz=quiz,
                        question_text=qtext,
                        defaults={
                            'option1': o1,
                            'option2': o2,
                            'option3': o3,
                            'option4': o4,
                            'correct_option': cor,
                            'explanation': exp,
                        }
                    )

            # Assignment
            if cdata.get('assignment'):
                adata = cdata['assignment']
                Assignment.objects.get_or_create(
                    course=course,
                    title=adata['title'],
                    defaults={
                        'description': adata['description'],
                        'max_marks': adata['max_marks'],
                    }
                )

        # 6. Student Enrollments & Progress for student_alex
        first_course = created_courses[0]
        enrollment, _ = Enrollment.objects.get_or_create(user=student, course=first_course)
        for lesson in first_course.lessons.all()[:2]:
            LessonProgress.objects.get_or_create(user=student, lesson=lesson, defaults={'completed': True})

        # Completed course for Certificate demo
        second_course = created_courses[3]  # AI course
        enr2, _ = Enrollment.objects.get_or_create(
            user=student,
            course=second_course,
            defaults={'completed': True}
        )
        enr2.completed = True
        enr2.save()
        for l in second_course.lessons.all():
            LessonProgress.objects.get_or_create(user=student, lesson=l, defaults={'completed': True})

        Certificate.objects.get_or_create(user=student, course=second_course)

        # Sample Contact Message
        ContactMessage.objects.get_or_create(
            email='partner@techcorp.com',
            defaults={
                'name': 'Corporate Partnerships',
                'subject': 'Enterprise Training Inquiry',
                'message': 'We are looking to onboard 50 engineers into the Python Django and DevOps tracks.'
            }
        )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully with all 8 educational topics and local images!"))
