# 🪟 SpotMe - Windows Setup Guide

Ghid special pentru instalare și troubleshooting pe Windows.

---

## ⚠️ Important pentru Python 3.13

Dacă ai **Python 3.13**, unele pachete nu sunt încă compatibile. Urmează pașii ăștia:

### Instalare Pachete (Fără Pillow și psycopg2)

```powershell
cd backend

# Instalează pachetele esențiale
pip install Django==5.0.1
pip install djangorestframework==3.14.0
pip install djangorestframework-simplejwt==5.3.1
pip install django-cors-headers==4.3.1
pip install python-decouple==3.8
pip install django-cron==0.6.0
```

**SAU** folosește `requirements-windows.txt`:

```powershell
pip install -r requirements-windows.txt
```

---

## 🔧 Setup Complet Backend

### Pas 1: Instalare Dependențe

```powershell
cd C:\Users\YOUR_USERNAME\Desktop\JimBuddy\backend

# Instalează pachetele
pip install -r requirements-windows.txt
```

### Pas 2: Configurare .env

```powershell
# Copiază fișierul exemplu
copy .env.example .env

# Editează cu Notepad
notepad .env
```

Verifică că `.env` conține:

```env
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

USE_SQLITE=True

DB_NAME=spotme_db
DB_USER=spotme_user
DB_PASSWORD=spotme_password
DB_HOST=localhost
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Pas 3: Migrații și Setup

```powershell
# Rulează migrații
python manage.py migrate

# Creează admin user
python manage.py createsuperuser
# Username: admin
# Password: admin123

# Populează săli demo
python manage.py populate_demo_gyms

# Pornește serverul
python manage.py runserver
```

---

## 🎨 Setup Frontend

### Pas 1: Instalare Node.js

Dacă nu ai Node.js instalat:
1. Download de pe: https://nodejs.org/
2. Instalează versiunea **LTS** (18.x sau 20.x)
3. Restart PowerShell după instalare

### Pas 2: Instalare Dependențe

```powershell
cd ..\frontend

# Instalează pachete
npm install

# Verifică că .env există
notepad .env
```

Verifică că `.env` conține:

```env
VITE_API_URL=http://localhost:8000/api
```

### Pas 3: Pornește Frontend

```powershell
npm run dev
```

Frontend rulează la: `http://localhost:5173`

---

## 🐛 Troubleshooting Windows

### Eroare: `python` nu e recunoscut

**Soluție:**
```powershell
# Încearcă:
python3 manage.py runserver

# SAU
py manage.py runserver

# SAU
py -3.11 manage.py runserver  # Dacă ai Python 3.11
```

### Eroare: `pip` nu e recunoscut

**Soluție:**
```powershell
python -m pip install -r requirements-windows.txt
```

### Eroare: `ModuleNotFoundError: No module named 'decouple'`

**Soluție:**
```powershell
pip install python-decouple
```

### Eroare: CORS - `Access-Control-Allow-Origin` header missing

**Cauză:** CORS nu e configurat corect în settings.py

**Verificare:**
1. Deschide `backend\spotme_project\settings.py`
2. Scroll la final (după linia ~180)
3. Verifică că există:

```python
# CORS Configuration - FIXED pentru Development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
```

4. **IMPORTANT:** NU trebuie să existe `CORS_ALLOWED_ORIGINS = config(...)`
5. Restart backend după modificare

### Eroare: `404 Not Found: /api/sesiuni`

**Cauză:** Backend nu are `APPEND_SLASH = False`

**Soluție:**
1. Deschide `backend\spotme_project\settings.py`
2. După linia `ALLOWED_HOSTS`, adaugă:

```python
# Disable trailing slash requirement for API endpoints
APPEND_SLASH = False
```

3. Restart backend

### Eroare: Pillow sau psycopg2-binary nu se instalează

**Cauză:** Python 3.13 prea nou, pachetele incompatibile

**Soluție:** Nu sunt necesare pentru development! SQLite funcționează fără ele.

Dacă chiar vrei PostgreSQL:
- Instalează **Visual Studio Build Tools** de pe Microsoft
- SAU downgrade la **Python 3.11**

---

## ✅ Checklist Final

După toate fix-urile, verifică:

- [ ] Backend pornește fără erori: `python manage.py runserver`
- [ ] Vezi "Starting development server at http://127.0.0.1:8000/"
- [ ] Frontend pornește: `npm run dev`
- [ ] Vezi "Local: http://localhost:5173/"
- [ ] Poți accesa `http://localhost:5173` în browser
- [ ] Poți accesa `http://localhost:8000/admin` (admin/admin123)
- [ ] În browser Console (F12) NU vezi erori CORS
- [ ] Poți crea cont (Register) fără erori

---

## 📊 Verificare Rapidă API

Testează că backend-ul funcționează:

```powershell
# Test 1: Lista săli
curl http://localhost:8000/api/sali/

# Test 2: API root
curl http://localhost:8000/api/
```

Ar trebui să vezi JSON responses, nu erori 404 sau CORS.

---

## 🎯 Dacă Tot Nu Merge

### Reset Complet

```powershell
# Backend
cd backend
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_demo_gyms

# Frontend
cd ..\frontend
rmdir /s /q node_modules
rmdir /s /q dist
npm install
```

### Verifică Versiuni

```powershell
python --version    # Ar trebui Python 3.11 sau 3.13
node --version      # Ar trebui v18.x sau v20.x
npm --version       # Ar trebui 9.x sau 10.x
```

---

## 📞 Log Files pentru Debug

Dacă ceri ajutor, trimite aceste informații:

1. **Python version:** `python --version`
2. **Eroare din terminal backend** (copy-paste eroarea completă)
3. **Browser Console errors** (F12 → Console tab)
4. **Request în Network tab** (F12 → Network → Click pe request roșu)

---

**Happy Coding pe Windows! 💪🪟**
