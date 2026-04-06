# Simple LMS

Simple LMS adalah project **Learning Management System (LMS)** sederhana berbasis **Django**, **PostgreSQL**, dan **Docker**.

Project ini dibuat untuk memenuhi tugas **Capstone Progress 1 & Progress 2**:
- **Progress 1**: Docker & Django Foundation
- **Progress 2**: Database Design & ORM Implementation

---

## 🚀 Features

### Progress 1
- Setup project Django menggunakan Docker
- Konfigurasi PostgreSQL di Docker
- Environment variables untuk database
- Django dapat diakses di `localhost:8000`

### Progress 2
- User role management (`admin`, `instructor`, `student`)
- Category hierarchy (self-referencing)
- Course dan Lesson management
- Student Enrollment
- Lesson Progress Tracking
- Query Optimization dengan `select_related()` dan `prefetch_related()`
- Django Admin configuration
- Initial data fixtures

---

## 📂 Project Structure

```bash
simple-lms/
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── manage.py
├── README.md
├── lms_fixture.json
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── lms/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── query_demo.py
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py
    └──
```

---

## ⚙️ Tech Stack

- **Python 3.10**
- **Django 4.x**
- **PostgreSQL 15**
- **Docker**
- **Docker Compose**

---

## 🔧 Cara Menjalankan Project

### 1. Clone Repository
```bash
git clone <repo-url>
cd simple-lms
```

### 2. Jalankan Docker
```bash
docker-compose up --build
```

### 3. Jalankan Migration
```bash
docker-compose exec web python manage.py migrate
```

### 4. Buat Superuser (Opsional)
```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Akses Project
- **Django App** → http://localhost:8000
- **Django Admin** → http://localhost:8000/admin

---

## 🗄️ Environment Variables

Project ini menggunakan environment variables untuk koneksi database PostgreSQL.

### Contoh konfigurasi:
```env
DB_NAME=lms_db
DB_USER=lms_user
DB_PASSWORD=lms_pass
DB_HOST=db
DB_PORT=5432
```

---

## 🧩 Data Models

Project ini memiliki beberapa model utama:

### 1. UserProfile
Menambahkan role pada user Django:
- `admin`
- `instructor`
- `student`

### 2. Category
Model kategori yang mendukung **hierarchy / parent-child** menggunakan self-referencing relationship.

### 3. Course
Setiap course memiliki:
- title
- description
- instructor
- category

### 4. Lesson
Setiap lesson:
- terhubung ke course
- memiliki urutan (`order`)

### 5. Enrollment
Menghubungkan student dengan course.

**Constraint:**
- satu student tidak bisa mengambil course yang sama lebih dari satu kali

### 6. Progress
Melacak penyelesaian lesson oleh student.

---

## ⚡ Query Optimization

Project ini menggunakan custom QuerySet untuk optimasi query database.

### 1. Course Listing
```python
Course.objects.for_listing()
```

Optimasi yang digunakan:
- `select_related()`
- `annotate()`

Digunakan untuk:
- mengambil instructor
- mengambil category
- menghitung jumlah lesson
- menghitung jumlah student

### 2. Student Dashboard
```python
Enrollment.objects.for_student_dashboard()
```

Optimasi yang digunakan:
- `select_related()`
- `prefetch_related()`

Digunakan untuk:
- student
- course
- category
- instructor
- lessons
- progress records

---

## 🧪 Query Optimization Demo

File demo tersedia di:

```bash
lms/query_demo.py
```

### Cara menjalankan demo

#### PowerShell (Windows)
```powershell
Get-Content lms/query_demo.py | docker-compose exec -T web python manage.py shell
```

#### CMD / Bash
```bash
docker-compose exec -T web python manage.py shell < lms/query_demo.py
```

### Hasil Query Comparison
Berdasarkan pengujian pada project ini:

- **N+1 version** → `28 queries`
- **Optimized version** → `1 query`
- **Dashboard optimized** → `3 queries`

Demo ini menunjukkan perbedaan performa antara query biasa dan query yang telah dioptimasi menggunakan:
- `select_related()`
- `prefetch_related()`

---

## 🛠️ Django Admin Configuration

Django Admin telah dikonfigurasi dengan fitur:

- `list_display`
- `search_fields`
- `list_filter`
- inline `Lesson` pada `Course`

### Admin Models
- UserProfile
- Category
- Course
- Lesson
- Enrollment
- Progress

---

## 📦 Fixtures

Project ini menyediakan **initial dummy data** dalam bentuk fixture JSON.

### Export dummy data
```powershell
docker-compose exec web python manage.py dumpdata lms --indent 4 > lms_fixture.json
```

### Load dummy data
```powershell
docker-compose exec web python manage.py loaddata lms_fixture.json
```

---

## 📸 Screenshots

Tambahkan screenshot berikut pada repository / dokumentasi:
- Django welcome page
- Django admin dashboard
- Query optimization demo result

---

## 📌 Submission

Project ini diupload ke repository **GitHub/GitLab** dan link repository dikumpulkan melalui **KULINO**.

---

## 👨‍💻 Author

Dibuat sebagai bagian dari tugas **Simple LMS Capstone Project** menggunakan **Django ORM**, **PostgreSQL**, dan **Docker**.
