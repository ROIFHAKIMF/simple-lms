# Simple LMS

Simple LMS adalah project **Learning Management System (LMS)** sederhana berbasis **Django**, **PostgreSQL**, dan **Docker**.

---

## 🚀 Features per Progress

### Progress 1 — Docker & Django Foundation
- Setup project Django menggunakan Docker
- Konfigurasi PostgreSQL di Docker
- Environment variables untuk database
- Django dapat diakses di `localhost:8000`

### Progress 2 — Database Design & ORM Implementation
- User role management (`admin`, `instructor`, `student`)
- Category hierarchy (self-referencing)
- Course & Lesson management
- Student Enrollment
- Lesson Progress Tracking
- Query Optimization dengan `select_related()` dan `prefetch_related()`
- Django Admin configuration

### Progress 3 — REST API & Authentication System ✅
- REST API lengkap menggunakan **Django Ninja**
- **JWT Authentication** (access token + refresh token)
- **Role-Based Access Control** (`@is_instructor`, `@is_admin`, `@is_student`)
- **Pydantic schema validation** untuk semua endpoint
- **Swagger UI** di `/api/docs`
- **Postman Collection** untuk testing semua endpoint

---

## 📂 Project Structure

```
simple-lms/
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── manage.py
├── README.md
├── lms_fixture.json
├── Simple_LMS_API.postman_collection.json   ← NEW (Progress 3)
├── config/
│   ├── settings.py
│   └── urls.py
└── lms/
    ├── models.py
    ├── admin.py
    ├── api.py           ← NEW — NinjaAPI entrypoint
    ├── auth_utils.py    ← NEW — JWT helpers
    ├── permissions.py   ← NEW — JWTAuth + role decorators
    ├── schemas.py       ← NEW — Pydantic schemas
    ├── query_demo.py
    ├── routers/         ← NEW
    │   ├── auth.py
    │   ├── courses.py
    │   └── enrollments.py
    └── migrations/
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10 |
| Framework | Django 4.2 |
| REST API | Django Ninja 1.3 |
| Auth | PyJWT 2.8 |
| Database | PostgreSQL 15 |
| Container | Docker / Docker Compose |

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

### 4. (Opsional) Load Fixture Data
```bash
docker-compose exec web python manage.py loaddata lms_fixture.json
```

### 5. Akses Project
| URL | Keterangan |
|---|---|
| http://localhost:8000/admin | Django Admin |
| http://localhost:8000/api/docs | **Swagger UI** |

---

## 🔐 API — Authentication

### Register
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "budi",
  "email": "budi@example.com",
  "password": "rahasia123",
  "role": "student"
}
```

### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "budi",
  "password": "rahasia123"
}
```
Response:
```json
{
  "access_token": "<jwt>",
  "refresh_token": "<jwt>",
  "token_type": "bearer"
}
```

### Menggunakan Token
Sertakan header berikut di semua request yang memerlukan autentikasi:
```
Authorization: Bearer <access_token>
```

---

## 📋 API Endpoints

### Auth (`/api/auth/`)
| Method | Path | Keterangan | Auth |
|---|---|---|---|
| POST | `/register` | Daftar user baru | — |
| POST | `/login` | Login, dapat JWT | — |
| POST | `/refresh` | Refresh access token | — |
| GET | `/me` | Profil user saat ini | ✅ |
| PUT | `/me` | Update profil | ✅ |

### Courses (`/api/courses/`)
| Method | Path | Keterangan | Auth | Role |
|---|---|---|---|---|
| GET | `/` | List courses (pagination + filter) | — | — |
| GET | `/{id}` | Detail course | — | — |
| POST | `/` | Buat course | ✅ | instructor / admin |
| PATCH | `/{id}` | Update course | ✅ | owner / admin |
| DELETE | `/{id}` | Hapus course | ✅ | admin |

#### Query Parameters untuk List Courses
| Param | Tipe | Default | Keterangan |
|---|---|---|---|
| `page` | int | 1 | Halaman |
| `page_size` | int | 10 | Item per halaman (max 100) |
| `search` | string | — | Filter berdasarkan judul |
| `category_id` | int | — | Filter berdasarkan kategori |

### Enrollments (`/api/enrollments/`)
| Method | Path | Keterangan | Auth | Role |
|---|---|---|---|---|
| POST | `/` | Enroll ke course | ✅ | student / admin |
| GET | `/my-courses` | Courses yang diikuti | ✅ | any |
| POST | `/{id}/progress` | Tandai lesson selesai | ✅ | any |

---

## 🛡️ Role-Based Access Control

| Role | Register/Login | Create Course | Update Course | Delete Course | Enroll |
|---|---|---|---|---|---|
| **student** | ✅ | ❌ | ❌ | ❌ | ✅ |
| **instructor** | ✅ | ✅ | ✅ (own) | ❌ | ❌ |
| **admin** | ✅ | ✅ | ✅ (all) | ✅ | ✅ |

---

## 📖 Swagger UI

Akses dokumentasi interaktif di:

```
http://localhost:8000/api/docs
```

Fitur:
- Semua endpoint terdokumentasi otomatis
- Bisa langsung test dari browser
- Input schema validation terlihat jelas
- Tombol **Authorize** untuk JWT token

---

## 📦 Postman Collection

File: `Simple_LMS_API.postman_collection.json`

### Import ke Postman
1. Buka Postman → **Import**
2. Pilih file `Simple_LMS_API.postman_collection.json`
3. Jalankan **Login** → token otomatis tersimpan ke collection variable `token`
4. Semua request protected otomatis menggunakan token

### Flow Testing
```
Register (instructor) → Login → Create Course
Register (student)    → Login → Enroll → My Courses → Mark Progress
```

---

## 🗄️ Environment Variables

```env
DB_NAME=lms_db
DB_USER=lms_user
DB_PASSWORD=lms_pass
DB_HOST=db
DB_PORT=5432
```

---

## 👨‍💻 Author

Dibuat sebagai bagian dari tugas **Simple LMS Capstone Project** — Progress 3: REST API & Authentication System.