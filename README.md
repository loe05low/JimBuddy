# SpotMe - Gym Buddy Finder

**Aplicație pentru găsirea partenerilor de antrenament la sală**

SpotMe permite utilizatorilor să găsească parteneri de antrenament (gym buddies) în funcție de locație și preferințe, să creeze sesiuni de antrenament, să primească cereri de la alți utilizatori, și să ofere rating/feedback după fiecare sesiune.

---

## 📋 Tehnologii Utilizate

### Backend
- **Django 5.0.1** - Framework web Python
- **Django REST Framework** - API RESTful
- **JWT (SimpleJWT)** - Autentificare
- **PostgreSQL/SQLite** - Bază de date
- **django-cron** - Task-uri programate

### Frontend (În dezvoltare)
- **React** - UI Framework
- **Tailwind CSS** - Styling
- **React Leaflet** - Hartă interactivă (OpenStreetMap)

---

## 🚀 Instalare și Configurare

### Cerințe
- Python 3.11+
- Node.js 18+ (pentru frontend)
- PostgreSQL 14+ (opțional, implicit se folosește SQLite)

### 1. Backend Setup

```bash
cd backend

# Instalare dependențe
pip install -r requirements.txt

# Configurare environment variables
cp .env.example .env
# Editează .env cu configurările tale

# Rulează migrații
python manage.py migrate

# Creează superuser pentru admin panel
python manage.py createsuperuser

# Populează săli demo (8 săli în București)
python manage.py populate_demo_gyms

# Pornește serverul
python manage.py runserver
```

**Backend rulează la:** `http://localhost:8000`

**Admin Panel:** `http://localhost:8000/admin`
- Username: `admin`
- Password: `admin123` (schimbă în producție!)

### 2. Configurare Bază de Date

#### Opțiunea 1: SQLite (Development - Implicit)
```env
USE_SQLITE=True
```

#### Opțiunea 2: PostgreSQL (Production)
```env
USE_SQLITE=False
DB_NAME=spotme_db
DB_USER=spotme_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

Creează database PostgreSQL:
```bash
psql -U postgres
CREATE DATABASE spotme_db;
CREATE USER spotme_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE spotme_db TO spotme_user;
\q
```

---

## 📡 API Endpoints

### Base URL: `http://localhost:8000/api`

### Autentificare

| Method | Endpoint | Descriere | Autentificare |
|--------|----------|-----------|---------------|
| POST | `/auth/register` | Înregistrare utilizator nou | Nu |
| POST | `/auth/login` | Login (obține JWT token) | Nu |
| POST | `/auth/refresh` | Reîmprospătează JWT token | Nu |
| GET | `/auth/me` | Informații utilizator curent | Da |

#### Exemplu Register
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "nume": "John Doe",
    "grad": "Intermediar"
  }'
```

#### Exemplu Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'

# Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Săli (Gyms)

| Method | Endpoint | Descriere | Autentificare |
|--------|----------|-----------|---------------|
| GET | `/sali` | Listează toate sălile pentru hartă | Nu |
| GET | `/sali/{id}` | Detalii sală | Nu |

### Sesiuni de Antrenament

| Method | Endpoint | Descriere | Autentificare |
|--------|----------|-----------|---------------|
| GET | `/sesiuni?status=activ` | Listează sesiuni active | Da |
| POST | `/sesiuni` | Creează sesiune nouă | Da |
| GET | `/sesiuni/{id}` | Detalii sesiune | Da |
| GET | `/sesiuni/my_sessions` | Sesiunile mele | Da |

#### Exemplu Creare Sesiune
```bash
curl -X POST http://localhost:8000/api/sesiuni \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "sala": "684ffa0b-5095-4a93-a072-6dbae8c68288",
    "tip_antrenament": "Cardio & Forță",
    "interval_orar": "18:00 - 20:00",
    "descriere": "Sesiune intensă, focus pe piept și brațe",
    "data_expirare": "2025-11-07T20:00:00Z"
  }'
```

### Cereri Gym Buddy

| Method | Endpoint | Descriere | Autentificare |
|--------|----------|-----------|---------------|
| GET | `/cereri` | Cererile mele (trimise + primite) | Da |
| POST | `/cereri` | Trimite cerere gym buddy | Da |
| PATCH | `/cereri/{id}` | Acceptă/refuză cerere | Da (doar owner sesiune) |

#### Exemplu Trimitere Cerere
```bash
curl -X POST http://localhost:8000/api/cereri \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "sesiune": "SESIUNE_UUID"
  }'
```

#### Exemplu Acceptare Cerere
```bash
curl -X PATCH http://localhost:8000/api/cereri/{cerere_id} \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "acceptat"
  }'
```

### Profiluri

| Method | Endpoint | Descriere | Autentificare |
|--------|----------|-----------|---------------|
| GET | `/profiles` | Listează toate profilurile | Nu |
| GET | `/profiles/{id}` | Detalii profil utilizator | Nu |
| GET | `/profiles/{id}/ratings` | Rating-uri primite de utilizator | Nu |
| GET | `/profiles/{id}/sesiuni` | Istoric sesiuni utilizator | Nu |
| GET | `/profiles/me` | Profilul meu | Da |
| PATCH | `/profiles/me` | Actualizează profilul meu | Da |

### Rating-uri

| Method | Endpoint | Descriere | Autentificare |
|--------|----------|-----------|---------------|
| GET | `/rating` | Listează toate rating-urile | Da |
| POST | `/rating` | Adaugă rating după sesiune | Da |

#### Exemplu Adăugare Rating
```bash
curl -X POST http://localhost:8000/api/rating \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to_user": 2,
    "sesiune": "SESIUNE_UUID",
    "rating": 4.5,
    "comentariu": "Partener excelent! Motivant și profesionist."
  }'
```

---

## 🔐 Autentificare JWT

Toate request-urile autentificate trebuie să includă header-ul:
```
Authorization: Bearer YOUR_JWT_ACCESS_TOKEN
```

Token-urile JWT au următoarele durate:
- **Access Token:** 1 zi
- **Refresh Token:** 7 zile

---

## 👤 Profiluri Utilizator

### Câmpuri Profil
```json
{
  "id": 1,
  "nume": "John Doe",
  "poza": "https://example.com/photo.jpg",
  "rating": 4.8,
  "nr_antrenamente": 25,
  "grad": "Intermediar",
  "created_at": "2025-11-06T12:00:00Z"
}
```

### Grade Disponibile
- Începător
- Intermediar
- Avansat
- Sportiv
- Expert
- Veteran

---

## 🏋️ Fluxul Aplicației

### 1. Înregistrare și Login
```
User → Register (/api/auth/register)
     → Login (/api/auth/login)
     → Obține JWT Token
```

### 2. Creare Sesiune Antrenament
```
User → Selectează Sală pe Hartă (/api/sali)
     → Creează Sesiune (/api/sesiuni)
     → Sesiunea apare pe hartă (status: activ)
```

### 3. Trimitere Cerere Gym Buddy
```
User → Vezi Sesiuni Active (/api/sesiuni?status=activ)
     → Vezi Profil Owner (/api/profiles/{id})
     → Trimite Cerere (/api/cereri)
```

### 4. Acceptare/Refuzare Cerere
```
Owner → Vezi Cereri Primite (/api/cereri)
      → Vezi Profil Applicant
      → Acceptă/Refuză (/api/cereri/{id})
```

### 5. Rating după Antrenament
```
Participanți → Finalizează Sesiune
             → Adaugă Rating (/api/rating)
             → Rating actualizat automat pentru ambii
```

---

## 🔄 Arhivare Automată Sesiuni

**Cron Job** arhivează automat sesiunile expirate la fiecare oră.

### Rulare Manuală Cron Job
```bash
python manage.py runcrons
```

### Arhivare Manuală din Admin Panel
1. Accesează `http://localhost:8000/admin`
2. Mergi la **Sesiuni de Antrenament**
3. Selectează sesiunile
4. Actions → **Arhivează sesiunile selectate**

---

## 🗺️ Săli Demo

Aplicația vine cu **8 săli pre-populate** în București:

1. **World Class Victoriei** - Bulevardul Lascăr Catargiu 15
2. **GymBox Obor** - Bulevardul Ferdinand 30
3. **Iron Gym Militari** - Strada Iuliu Maniu 7
4. **Gold's Gym Universitate** - Bulevardul Regina Elisabeta 35
5. **FitLife Unirii** - Piața Unirii 1
6. **CrossFit Arena Pipera** - Șoseaua București-Ploiești 42D
7. **PowerGym Timpuri Noi** - Bulevardul Timișoara 26
8. **Body & Mind Fitness Herastrau** - Strada Aviator Popisteanu 54A

Pentru a re-popula sau actualiza:
```bash
python manage.py populate_demo_gyms
```

---

## 🛡️ Permisiuni și Securitate

### Permisiuni API
- **Săli:** Public (read-only)
- **Sesiuni:** Autentificat (create/read)
- **Cereri:** Autentificat (create/read/update)
- **Rating:** Autentificat (create/read)
- **Profile:** Public read, autentificat write (doar propriul profil)

### Validări
- Parolă minimum 6 caractere
- Rating între 1.0 și 5.0
- Un user poate trimite o singură cerere per sesiune
- Un user poate da un singur rating per sesiune
- Doar owner-ul sesiunii poate accepta/refuza cereri

---

## 🐛 Debugging și Development

### Verificare API
```bash
# Test API disponibilitate
curl http://localhost:8000/api/sali/

# Test cu autentificare
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Django Shell
```bash
python manage.py shell

# Testare models
from users.models import UserProfile
from gyms.models import Sala
profiles = UserProfile.objects.all()
sali = Sala.objects.all()
```

### Logs
```bash
# Vezi output server
python manage.py runserver --verbosity 3
```

---

## 📦 Structura Proiectului

```
backend/
├── manage.py
├── requirements.txt
├── .env
├── spotme_project/        # Django project settings
│   ├── settings.py
│   └── urls.py
├── users/                 # User profiles & auth
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── admin.py
├── gyms/                  # Gyms/Săli
│   ├── models.py
│   ├── management/commands/
│   │   └── populate_demo_gyms.py
│   └── ...
├── workouts/              # Sessions & Requests
│   ├── models.py
│   ├── cron.py            # Auto-archive cron job
│   └── ...
└── ratings/               # Ratings & Comments
    └── ...

frontend/                  # (În dezvoltare)
```

---

## 🚧 TODO / Roadmap

- [x] Backend Django REST API
- [x] Autentificare JWT
- [x] Admin Panel
- [x] Cron job arhivare
- [x] Săli demo
- [ ] React Frontend
- [ ] Hartă interactivă Leaflet
- [ ] UI Components (Tailwind)
- [ ] Integrare complete frontend-backend
- [ ] Testing (Unit + Integration)
- [ ] Deployment (Docker/Heroku)

---

## 📄 Licență

MIT License - Proiect educațional

---

## 👨‍💻 Autor

Dezvoltat pentru **SpotMe** - Gym Buddy Finder Application

**Contact Admin:**
- Admin Panel: http://localhost:8000/admin
- Username: `admin`
- Password: `admin123`

---

## 🆘 Support

Pentru probleme sau întrebări:
1. Verifică că serverul Django rulează: `python manage.py runserver`
2. Verifică migrațiile: `python manage.py migrate`
3. Verifică environment variables în `.env`
4. Consultă logs pentru erori

**Happy Spotting! 💪🏋️**
