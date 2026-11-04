# EduVibe - Modern Learning Management System (LMS)

A modern, responsive, and full-featured Learning Management System web application built with **Python Django**, **Bootstrap 5**, **JavaScript**, and **SQLite**.

---

## 🌟 Key Features

- **Responsive Design Across All Devices**: Seamless experience on Mobile smartphones, Tablets, and Desktops using Bootstrap 5.3 breakpoints and responsive components.
- **Course Discovery & Filtering**: Live search, category filtering, skill level filters, price tags, and sorting (Newest, Popular, Highest Rated, Price).
- **Interactive Course Player**:
  - Distraction-free video and lesson notes reading layout.
  - Interactive "Mark as Completed" button powered by asynchronous JavaScript (AJAX).
  - Dynamic progress tracking bar (0% - 100%).
  - Next / Previous lesson navigation.
  - Collapsible curriculum drawer with completion checkmarks.
- **Student Dashboard**:
  - Enrolled courses with visual progress bars.
  - Summary metrics: Total Enrolled, In Progress, Completed Courses, and Certificates.
  - Quick action buttons to resume learning.
- **Instructor Portal**:
  - Manage authored courses and track enrolled student counts directly from the dashboard.
- **Student Reviews & Star Ratings**:
  - Verified course reviews with 1 to 5 star ratings.
- **Authentication & User Profiles**:
  - Registration with Student / Instructor role selection.
  - Profile customization: avatar upload, headline, bio, and phone number.
- **Contact & Help Center**:
  - Functional contact form with user feedback alerts and interactive FAQ accordion.
- **Pre-populated Demo Data**:
  - Includes `python manage.py seed_data` command with courses, instructors, lessons, and reviews.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12, Django 5.2 (MTV architecture, ORM, Auth, Signals)
- **Frontend**: HTML5, CSS3, Bootstrap 5.3, Bootstrap Icons, JavaScript (ES6 fetch API)
- **Database**: SQLite (`db.sqlite3`)

---

## 🚀 Quick Start Guide

### 1. Run Database Migrations (already prepared)
```bash
python manage.py migrate
```

### 2. Populate Demo Courses & Accounts
```bash
python manage.py seed_data
```

### 3. Start the Development Server
```bash
python manage.py runserver
```

Now open your web browser and navigate to:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🔑 Demo Accounts

The project includes pre-configured demo users so you can test all features right away:

| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Student** | `student_alex` | `password123` | Enrolled in courses with active progress |
| **Instructor** | `instructor_john` | `password123` | Course author with course management view |
| **Admin** | `admin` | `admin123` | Access to `/admin/` management portal |

---

## 📁 Project Architecture

```
LMS/
├── accounts/               # User profiles, auth, and student dashboard
│   ├── forms.py            # Styled Bootstrap authentication & profile forms
│   ├── models.py           # User Profile model & role management
│   ├── views.py            # Login, register, dashboard, profile views
│   └── urls.py
├── core/                   # Marketing & informational pages
│   ├── forms.py            # Contact & newsletter forms
│   ├── models.py           # ContactMessage & Newsletter models
│   ├── views.py            # Home, About, Contact, Newsletter
│   └── urls.py
├── courses/                # Core LMS curriculum system
│   ├── management/commands/seed_data.py # Realistic demo data generator
│   ├── models.py           # Category, Course, Module, Lesson, Enrollment, Review
│   ├── views.py            # Catalog, detail, enrollment, lesson player, review
│   ├── context_processors.py # Global categories in navbar
│   └── urls.py
├── lms_project/            # Django root settings & URL router
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
│   ├── css/style.css       # Custom design system & responsive styling
│   └── js/main.js          # AJAX lesson completion, tooltips, alert dismissers
├── templates/
│   ├── base.html           # Master layout with Bootstrap 5.3 CDN
│   ├── navbar.html         # Responsive navigation bar
│   ├── footer.html         # Responsive footer with newsletter
│   ├── accounts/           # Login, Register, Dashboard, Profile templates
│   ├── core/               # Home, About, Contact templates
│   └── courses/            # Course List, Detail, and Lesson Player templates
├── manage.py
└── README.md
```

---

## 📱 Responsive Testing

The website is fully optimized for all screen sizes:
- **Mobile (< 576px)**: Offcanvas/collapsible navbar, single-column course cards, mobile-friendly touch targets.
- **Tablet (576px - 992px)**: 2-column adaptive layout, stacked learning viewer.
- **Desktop (> 992px)**: Multi-column grids, sticky curriculum sidebar, rich hero graphics.

