# Online Learning Management System (LMS)

A complete, professional, responsive Online Learning Management System built with **Python**, **Django 5**, **HTML5**, **CSS3**, **Bootstrap 5**, **JavaScript**, and **SQLite**.

---

## 🎨 Theme & Styling

- **Color Palette**:
  - Light Lavender (`#F5F3FF`, `#EDE9FE`, `#DDD6FE`)
  - Soft Purple (`#8B5CF6`, `#7C3AED`, `#6D28D9`)
  - Light Blue (`#E0F2FE`, `#38BDF8`, `#0284C7`)
  - Light Grey (`#F8FAFC`, `#F1F5F9`, `#E2E8F0`)
  - Dark Navy Text (`#0F172A`, `#1E1B4B`)
  - Pure White (`#FFFFFF`)
- **Design Elements**:
  - Clean light-colour background.
  - Modern cards with rounded corners.
  - Soft shadows and attractive buttons.
  - Fully responsive on mobile, tablet, and desktop screens.
  - Local image assets inside `online_app/static/online_app/images/` with no external URL dependencies.

---

## 📁 Required Architecture & Folder Structure

```
online_lms/
│
├── manage.py
├── db.sqlite3
├── requirements.txt
├── .gitignore
├── README.md
│
├── online_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── online_app/
    ├── migrations/
    │   └── 0001_initial.py
    ├── templates/
    │   └── online_app/
    │       ├── base.html
    │       ├── home.html
    │       ├── about.html
    │       ├── courses.html
    │       ├── course_detail.html
    │       ├── login.html
    │       ├── register.html
    │       ├── student_dashboard.html
    │       ├── instructor_dashboard.html
    │       ├── my_courses.html
    │       ├── lessons.html
    │       ├── quiz.html
    │       ├── assignments.html
    │       ├── certificates.html
    │       ├── profile.html
    │       ├── contact.html
    │       ├── course_form.html
    │       ├── course_confirm_delete.html
    │       ├── lesson_form.html
    │       ├── quiz_form.html
    │       ├── question_form.html
    │       └── assignment_form.html
    │
    ├── static/
    │   └── online_app/
    │       ├── css/
    │       │   ├── style.css
    │       │   ├── home.css
    │       │   ├── courses.css
    │       │   ├── auth.css
    │       │   ├── dashboard.css
    │       │   ├── lessons.css
    │       │   ├── quiz.css
    │       │   └── profile.css
    │       │
    │       ├── js/
    │       │   ├── main.js
    │       │   ├── dashboard.js
    │       │   └── quiz.js
    │       │
    │       └── images/
    │           ├── logo.png
    │           ├── hero.png
    │           ├── courses/
    │           │   ├── course1.png ... course6.png
    │           ├── instructors/
    │           │   ├── inst1.png ... inst4.png
    │           └── backgrounds/
    │               ├── pattern.png
    │               └── cta_bg.png
    │
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── admin.py
    ├── tests.py
    └── apps.py
```

---

## 🌟 Core Features & Modules

### 1. Student Features
- **Registration, Login, and Logout**: Role-based authentication using Django's auth system.
- **Student Dashboard**: Metric cards for enrolled courses, in-progress count, completed courses, and certificates earned.
- **Course Catalog & Filtering**: Real-time keyword search, subject category filter, skill level selection, and price filter.
- **Course Detail & Enrollment**: Complete syllabus preview, lesson list, instructor spotlight, and 1-click database enrollment.
- **My Courses**: Enrolled courses with real-time percentage progress bars.
- **Lesson Player**: Responsive video player (16:9), study notes reading area, PDF download support, next/prev lesson navigation, and asynchronous AJAX "Mark as Completed" button.
- **Online Quizzes**: Multiple choice question engine, real-time score calculation, pass/fail grading based on pass mark thresholds, and question explanations.
- **Assignments**: Submit written solutions or upload files, view submission status and instructor feedback.
- **Certificates**: Automatically issued upon course completion with verification codes and print/PDF download capabilities.
- **Profile Management**: Update name, email, avatar image, phone number, headline, and biography.

### 2. Instructor Features
- **Instructor Dashboard**: Overview of courses taught, total student enrollments, and recent student activity.
- **Course Management (CRUD)**: Create, edit, and delete courses with thumbnail uploads and pricing.
- **Lesson Management**: Add video embed URLs, lesson reading notes, order, and PDF study materials.
- **Quiz Management**: Create quizzes and multiple-choice questions with answer keys and explanations.
- **Assignment Creation**: Create assignments with prompts, deadlines, and maximum marks.
- **Student Tracking**: Monitor enrolled student progress per course.

### 3. Django Admin Panel
Configured to manage:
- User Profiles (Students, Instructors, Admins)
- Categories
- Courses
- Lessons & Lesson Progress
- Enrollments
- Quizzes, Questions & Quiz Results
- Assignments & Assignment Submissions
- Certificates
- Contact Messages

---

## 🚀 How to Run the Website

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Database Migrations
```bash
python manage.py migrate
```

### 3. Populate Demo Data (Optional / Pre-loaded)
```bash
python manage.py seed_data
```

### 4. Start the Django Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🔑 Pre-Configured Test Accounts

| Role | Username | Password | Key Capability |
| :--- | :--- | :--- | :--- |
| **Student** | `student_alex` | `password123` | Enrolled in courses, can take quizzes, view certificates |
| **Instructor** | `instructor_john` | `password123` | Full access to Instructor Studio, create/edit courses |
| **Admin** | `admin` | `admin123` | Full access to `/admin/` management portal |

---

## 🧪 Testing

To run the automated test suite:
```bash
python manage.py test
```
All 6 comprehensive test cases verify public pages, student enrollment, lesson progress, quiz scoring, assignment submissions, and instructor CRUD operations.
