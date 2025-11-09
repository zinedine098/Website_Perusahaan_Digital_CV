---

# Dokumentasi Aplikasi Kursus Online (Django & Bootstrap)

## 1. Tinjauan Umum (Overview)

Aplikasi ini adalah platform pembelajaran online (Learning Management System - LMS) sederhana yang dibangun menggunakan framework Django untuk backend dan Bootstrap untuk frontend. Aplikasi ini memungkinkan instruktur untuk membuat dan mengelola kursus, serta memungkinkan siswa untuk mendaftar, mengakses materi, dan belajar.

**Target Pengguna:**
*   **Instruktur:** Membuat, mengedit, dan mengelola konten kursus.
*   **Siswa:** Mendaftar kursus, menonton video/materi, dan melacak progress pembelajaran.
*   **Admin:** Mengelola pengguna, kursus, dan konten secara keseluruhan melalui Django Admin.

**Tujuan Utama:**
*   Memberikan pengalaman belajar yang terstruktur dan mudah diakses.
*   Menyediakan antarmuka yang bersih dan responsif untuk pengelolaan kursus.
*   Membangun fondasi yang kuat untuk pengembangan fitur lebih lanjut di masa depan.

## 2. Fitur-Fitur Utama (Core Features)

Aplikasi akan memiliki fitur-fitur berikut, dibagi berdasarkan peran pengguna:

### A. Manajemen Pengguna (User Management)
*   **Registrasi:** Pengguna baru dapat mendaftar sebagai siswa atau instruktur.
*   **Login/Logout:** Sistem autentikasi yang aman.
*   **Profil Pengguna:** Setiap pengguna memiliki profil yang dapat diedit (nama, bio, foto).
*   **Peran (Roles):**
    *   **Siswa:** Dapat mendaftar dan mengakses kursus.
    *   **Instruktur:** Dapat membuat dan mengelola kursus miliknya.
    *   **Admin:** Akses penuh ke seluruh sistem.

### B. Manajemen Kursus (Course Management)
*   **Daftar Kursus:** Halaman publik yang menampilkan semua kursus yang tersedia, dengan fitur pencarian dan filter.
*   **Detail Kursus:** Halaman untuk setiap kursus yang menampilkan deskripsi, kurikulum (daftar modul & pelajaran), informasi instruktur, dan tombol untuk mendaftar.
*   **Pembuatan Kursus (Instruktur):** Form untuk instruktur membuat kursus baru (judul, deskripsi, gambar thumbnail).
*   **Pengelolaan Konten Kursus (Instruktur):**
    *   **Modul:** Mengelompokkan pelajaran dalam sebuah kursus (misal: "Pengenalan", "Dasar-Dasar").
    *   **Pelajaran (Lesson):** Konten individual dalam sebuah modul, bisa berupa video (embed dari YouTube/Vimeo), teks, atau file PDF.

### C. Pembelajaran & Interaksi (Learning & Interaction)
*   **Dashboard Siswa:** Halaman utama setelah login yang menampilkan kursus yang telah diikuti dan progress belajar.
*   **Halaman Pembelajaran:** Tampilan khusus untuk siswa yang mengikuti kursus, menampilkan daftar modul dan pelajaran.
*   **Konten Pelajaran:** Halaman untuk menampilkan konten dari setiap pelajaran (video player, teks, dll.) dengan navigasi ke pelajaran sebelumnya/berikutnya.
*   **Komentar pada Kursus:** Siswa dapat meninggalkan komentar atau pertanyaan di halaman detail kursus.

### D. Panel Admin (Admin Panel)
*   Menggunakan fitur bawaan Django Admin untuk:
    *   Mengelola data pengguna (menyetujui pendaftaran instruktur, dll.).
    *   Mengelola semua kursus, modul, dan pelajaran.
    *   Memoderasi komentar.

## 3. Teknologi yang Digunakan (Tech Stack)

*   **Backend:** Django 4.x (Python 3.x)
*   **Frontend:** Bootstrap 5, Material Design for Bootstrap (MDB)
*   **Database:** SQLite (sangat cocok untuk pengembangan lokal)
*   **Templating:** Django Template Engine (DTL)
*   **Pengelolaan Paket:** Pip & Virtualenv
*   **Editor Kode:** VS Code, PyCharm, atau sejenisnya.

## 4. Struktur Proyek (Project Structure)

Proyek akan diorganisir sebagai berikut untuk menjaga agar kode tetap bersih dan terstruktur:

```
nama_proyek/
├── manage.py
├── nama_proyek/          # Direktori konfigurasi proyek
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/                 # Folder untuk menyimpan semua aplikasi Django
│   ├── __init__.py
│   ├── users/            # Aplikasi untuk manajemen pengguna
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── templates/users/
│   ├── courses/          # Aplikasi untuk manajemen kursus & konten
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── templates/courses/
│   └── core/             # Aplikasi untuk utilitas umum (model abstrak, helper functions)
│       ├── __init__.py
│       └── models.py
├── static/               # Folder untuk file statis (CSS, JS, gambar)
│   ├── css/
│   ├── js/
│   └── images/
└── templates/            # Folder untuk template utama (base.html, index.html)
    ├── base.html
    ├── index.html
    └── partials/
```

## 5. Model Database (Database Models)

Berikut adalah rancangan model utama yang akan dibuat:

*   **`users.Profile`**: Model One-to-One dengan `User` bawaan Django untuk menambah informasi seperti `role` (siswa/instruktur), `bio`, dan `photo`.
*   **`courses.Course`**:
    *   `title` (CharField)
    *   `slug` (SlugField, untuk URL yang bersih)
    *   `description` (TextField)
    *   `instructor` (ForeignKey ke `User`)
    *   `thumbnail` (ImageField)
    *   `created_at` (DateTimeField)
*   **`courses.Module`**:
    *   `course` (ForeignKey ke `Course`)
    *   `title` (CharField)
    *   `order` (PositiveIntegerField, untuk mengurutkan modul)
*   **`courses.Lesson`**:
    *   `module` (ForeignKey ke `Module`)
    *   `title` (CharField)
    *   `content` (TextField, untuk teks atau embed video)
    *   `order` (PositiveIntegerField)
*   **`courses.Enrollment`**: Model "perantara" (intermediary) untuk mencatat siapa saja yang mengambil kursus apa.
    *   `student` (ForeignKey ke `User`)
    *   `course` (ForeignKey ke `Course`)
    *   `enrolled_at` (DateTimeField)
*   **`courses.Comment`**:
    *   `course` (ForeignKey ke `Course`)
    *   `user` (ForeignKey ke `User`)
    *   `body` (TextField)
    *   `created_at` (DateTimeField)

## 6. Konsep Desain UI/UX (Low-Fidelity)

Desain akan mengandalkan komponen Bootstrap untuk tampilan yang modern dan responsif.

*   **Halaman Beranda (`/`)**:
    *   Navbar dengan logo, link ke kursus, dan tombol Login/Register.
    *   Hero section dengan ajakan untuk mulai belajar.
    *   Grid "Kursus Unggulan".
    *   Footer.
*   **Halaman Daftar Kursus (`/courses/`)**:
    *   Search bar.
    *   Filter berdasarkan kategori (jika ada).
    *   Kartu Bootstrap untuk setiap kursus (menampilkan gambar, judul, instruktur, harga/hanya label "Gratis").
*   **Halaman Detail Kursus (`/courses/<slug>/`)**:
    *   Header dengan gambar kursus dan judul.
    *   Tab atau bagian untuk "Deskripsi", "Kurikulum", dan "Instruktur".
    *   Tombol "Daftar Sekarang".
    *   Kolom komentar di bagian bawah.
*   **Dashboard Siswa (`/dashboard/`)**:
    *   Sapaan personal.
    *   Daftar "Kursus Saya" dengan progress bar.
*   **Halaman Pembelajaran (`/courses/<slug>/learn/<lesson_id>/`)**:
    *   Layout dua kolom: sidebar navigasi (daftar modul & pelajaran) dan area konten utama (video atau teks).

## 7. Alur Pengembangan (Development Workflow)

1.  **Setup Lingkungan:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install django pillow
    ```
2.  **Inisiasi Proyek & Aplikasi:**
    ```bash
    django-admin startproject nama_proyek .
    mkdir apps
    python manage.py startapp users apps/users
    python manage.py startapp courses apps/courses
    python manage.py startapp core apps/core
    ```
3.  **Konfigurasi `settings.py`:** Tambahkan aplikasi baru ke `INSTALLED_APPS` dan konfigurasi `MEDIA_ROOT`, `MEDIA_URL`, `STATIC_ROOT`, `STATIC_URL`.
4.  **Buat Model:** Definisikan semua model di `apps/core/models.py`, `apps/users/models.py`, dan `apps/courses/models.py`.
5.  **Migrasi Database:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
6.  **Setup Admin:** Daftarkan model-model ke `admin.py` agar mudah diisi datanya.
7.  **Buat Superuser:**
    ```bash
    python manage.py createsuperuser
    ```
8.  **Kembangkan Fitur Bertahap:**
    *   Mulai dari **Manajemen Pengguna** (registrasi, login, profil).
    *   Lanjut ke **Manajemen Kursus** (buat model, tampilan di admin, tampilkan di halaman publik).
    *   Terakhir, bangun **Fitur Pembelajaran** (enrollment, halaman belajar).
9.  **Integrasi Bootstrap:** Unduh Bootstrap atau gunakan CDN, lalu buat `base.html` yang mengandung navbar dan footer. Gunakan komponen Bootstrap di template lainnya.

## 8. Menjalankan Aplikasi (Lokal)

Setelah pengembangan selesai, aplikasi dapat dijalankan dengan perintah sederhana:

1.  Pastikan virtual environment aktif.
2.  Jalankan migrasi (jika ada perubahan model):
    ```bash
    python manage.py migrate
    ```
3.  Jalankan server pengembangan:
    ```bash
    python manage.py runserver
    ```
4.  Buka browser dan akses `http://127.0.0.1:8000/`.

## 9. Pengembangan Selanjutnya (Future Enhancements)

Fitur-fitur ini bisa ditambahkan setelah versi dasar selesai:
*   **Sistem Pembayaran:** Integrasi dengan gateway pembayaran (Midtrans, Stripe).
*   **Quiz & Ujian:** Sistem kuis otomatis dengan penilaian.
*   **Sertifikat:** Generate sertifikat otomatis setelah kursus selesai.
*   **Notifikasi:** Email notifikasi untuk pendaftaran kursus, pesan baru, dll.
*   **Forum Diskusi:** Forum per-kursus untuk diskusi yang lebih mendalam.
*   **API Backend:** Menggunakan Django REST Framework untuk memungkinkan pengembangan aplikasi mobile (React Native, Flutter).



### 1. Fungsi dan Tujuan Utama Website

*   **Fungsi:** Sebagai platform Learning Management System (LMS) yang memungkinkan instruktur untuk **membuat, mengelola, dan mempublikasikan** kursus online, serta memungkinkan siswa untuk **mendaftar, mengakses, dan menyelesaikan** pembelajaran tersebut.
*   **Tujuan Utama:**
    *   Menyediakan wadah terpusat untuk pembelajaran daring yang terstruktur.
    *   Memberikan pengalaman belajar yang mudah diakses dan menyenangkan bagi siswa.
    *   Memberikan alat yang sederhana namun powerful bagi instruktur untuk berbagi ilmu.
    *   Membangun fondasi aplikasi yang solid dan dapat dikembangkan lebih lanjut.

### 2. Fitur-Fitur yang Diinginkan

Aplikasi akan memiliki fitur-fitur inti berikut:

*   **Manajemen Pengguna:**
    *   Registrasi akun baru (dengan pilihan peran: Siswa atau Instruktur).
    *   Sistem Login dan Logout yang aman.
    *   Halaman profil pengguna yang dapat diedit (nama, bio, foto).
*   **Manajemen Kursus (untuk Instruktur):**
    *   Membuat kursus baru (judul, deskripsi, gambar thumbnail).
    *   Mengorganisir konten kursus ke dalam **Modul** (contoh: "Bab 1: Pengenalan").
    *   Menambahkan **Pelajaran** ke dalam setiap modul (bisa berupa video embed, teks/artikel, atau file PDF).
*   **Katalog Kursus (untuk Siswa & Publik):**
    *   Halaman yang menampilkan daftar semua kursus yang tersedia.
    *   Fitur pencarian kursus berdasarkan judul.
    *   Halaman detail untuk setiap kursus yang menampilkan informasi lengkap, kurikulum, dan profil instruktur.
*   **Pembelajaran & Interaksi:**
    *   Sistem pendaftaran (enrollment) kursus oleh siswa.
    *   Dashboard khusus siswa yang menampilkan kursus yang sedang diambil.
    *   Halaman pembelajaran yang menampilkan konten pelajaran satu per satu dengan navigasi yang jelas.
    *   Fitur komentar atau diskusi di halaman detail kursus.
*   **Panel Admin:**
    *   Menggunakan Django Admin untuk mengelola seluruh data (pengguna, kursus, komentar) secara mudah.

### 3. Struktur Halaman

Berikut adalah peta halaman utama dan fungsinya:

1.  **Beranda (`/`):**
    *   Hero section dengan ajakan untuk belajar.
    *   Menampilkan beberapa kursus unggulan.
    *   Navigasi utama (navbar) ke Daftar Kursus, Login, dan Daftar.
2.  **Daftar Kursus (`/courses/`):**
    *   Grid atau daftar kartu (card) yang menampilkan semua kursus.
    *   Setiap kartu menampilkan: gambar kursus, judul, nama instruktur.
3.  **Detail Kursus (`/courses/<slug>/`):**
    *   Menampilkan gambar besar, judul, dan deskripsi lengkap kursus.
    *   Tab atau bagian terpisah untuk "Deskripsi", "Kurikulum" (daftar modul & pelajaran), dan "Tentang Instruktur".
    *   Tombol "Daftar Kursus" (jika siswa belum terdaftar).
    *   Bagian komentar di bagian bawah halaman.
4.  **Dashboard Siswa (`/dashboard/`):**
    *   Menampilkan sapaan personal.
    *   Daftar "Kursus Saya" dengan progress bar untuk setiap kursus.
5.  **Halaman Pembelajaran (`/courses/<slug>/learn/`):**
    *   Layout dua kolom:
        *   **Sidebar Kiri:** Daftar modul dan pelajaran dalam kursus.
        *   **Area Konten:** Menampilkan pelajaran yang sedang dibuka (video player atau teks).
6.  **Halaman Profil (`/profile/`):**
    *   Menampilkan dan mengedit informasi pengguna.
    *   Jika instruktur, menampilkan daftar kursus yang telah dibuat.
7.  **Halaman Login & Register (`/login/`, `/register/`):**
    *   Form standar untuk autentikasi dan pendaftaran pengguna baru.

### 4. Desain atau Layout yang Diinginkan

*   **Framework:** **Bootstrap 5**. Ini akan menjadi fondasi utama untuk styling.
*   **Gaya Visual:** Modern, bersih, profesional, dan **minimalis**. Fokus pada keterbacaan dan kemudahan navigasi.
*   **Responsivitas:** Wajib responsif. Tampilan harus optimal di berbagai ukuran layar, terutama desktop dan tablet/mobile.
*   **Komponen Kunci:**
    *   **Navbar:** Tetap di bagian atas, jelas, dan mudah digunakan.
    *   **Kartu (Cards):** Digunakan secara ekstensif untuk menampilkan kursus di halaman daftar.
    *   **Sidebar:** Digunakan pada halaman pembelajaran untuk navigasi konten.
    *   **Progress Bar:** Menunjukkan sejauh mana siswa telah menyelesaikan sebuah kursus.
    *   **Typography:** Menggunakan font default Bootstrap yang sudah baik untuk keterbacaan.

### 5. Fungsionalitas Khusus

*   **Akses Berdasarkan Peran (Role-Based Access Control):**
    *   Hanya **Instruktur** yang bisa membuat dan mengedit kursus miliknya.
    *   Hanya **Siswa** yang sudah mendaftar yang bisa mengakses halaman pembelajaran.
    *   **Admin** memiliki akses penuh melalui Django Admin.
*   **Penyajian Konten Terstruktur:**
    *   Sistem hierarki **Kursus > Modul > Pelajaran** untuk mengorganisir materi secara logis dan mudah diikuti.
*   **Integrasi Video Pihak Ketiga:**
    *   Untuk kesederhanaan (karena dijalankan lokal), konten video tidak akan di-hosting di server. Sebaliknya, aplikasi akan menggunakan **fitur embed** dari platform seperti YouTube atau Vimeo. Instruktur hanya perlu memasukkan URL embed-nya.