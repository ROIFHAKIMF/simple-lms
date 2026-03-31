# 📚 Simple LMS - Docker & Django Foundation

Project ini merupakan tahap awal pengembangan **Simple LMS (Learning Management System)** menggunakan **Django**, **Docker**, dan **PostgreSQL**.

Tujuan dari project ini adalah menyiapkan environment development yang terstruktur, portable, dan mudah dijalankan menggunakan containerization.

---

## 🎯 Learning Objectives
Pada progress ini, tujuan yang ingin dicapai adalah:

- Memahami konsep **containerization** menggunakan Docker
- Mampu membuat dan menjalankan **Dockerfile** dan **docker-compose.yml**
- Menginisialisasi project **Django** dengan struktur yang rapi
- Menghubungkan Django dengan **PostgreSQL**
- Menggunakan **environment variables** untuk konfigurasi project

---

## 🛠️ Tech Stack

- **Python 3.10**
- **Django**
- **PostgreSQL**
- **Docker**
- **Docker Compose**

---

## 📁 Project Structure

```bash
simple-lms/
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── requirements.txt
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── README.md