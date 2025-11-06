# 🚀 SpotMe - Quick Start Guide

## ✅ Setup Complete!

Toate erorile au fost rezolvate și backend-ul este gata de utilizare.

## 📝 Credențiale de Login

### Admin User (pentru Django Admin):
```
Username: admin
Password: admin123
URL: http://localhost:8000/admin/
```

### Regular User (pentru aplicație):
```
Username: testuser
Password: test123
```

## 🔧 Pornire Server

### Backend:
```bash
cd backend
python manage.py runserver
```

Serverul va porni pe: **http://localhost:8000**

### Frontend:
```bash
cd frontend
npm run dev
```

Frontend-ul va porni pe: **http://localhost:5173**

## 🧪 Testare Login

### Opțiune 1: Prin Frontend
1. Pornește backend-ul și frontend-ul
2. Deschide http://localhost:5173
3. Login cu:
   - **Username:** `testuser`
   - **Password:** `test123`

### Opțiune 2: Prin Postman/Insomnia (testare API directă)

**Login Request:**
```
POST http://localhost:8000/api/auth/login/
Content-Type: application/json

Body:
{
  "username": "testuser",
  "password": "test123"
}
```

**Răspuns Success:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## 🔐 Folosire Token

După login, salvează `access` token-ul și folosește-l în toate request-urile:

```
Authorization: Bearer {access_token}
```

Exemplu:
```
GET http://localhost:8000/api/profiles/me/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## 📡 API Endpoints Disponibile

### Authentication:
- `POST /api/auth/login/` - Login
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/refresh/` - Refresh token
- `GET /api/auth/me/` - Current user info

### Profile:
- `GET /api/profiles/me/` - Get your profile
- `PATCH /api/profiles/me/` - Update profile (avatar, bio, city, etc.)
- `GET /api/profiles/search?q=name` - Search users
- `POST /api/profiles/{id}/block/` - Block user
- `GET /api/profiles/{id}/achievements/` - Get user achievements

### Sessions:
- `GET /api/sesiuni/` - List sessions (cu filtre: status, tip, city, date, sort)
- `POST /api/sesiuni/` - Create session
- `POST /api/sesiuni/{id}/join/` - Join session
- `POST /api/sesiuni/{id}/complete_session/` - Complete session (AUTO TRACKING!)
- `GET /api/sesiuni/history/` - Your completed sessions

### Chat:
- `GET /api/conversations/` - List conversations
- `POST /api/conversations/create_private/` - Create private chat
- `GET /api/messages?conversation={id}` - Get messages

### Achievements & Goals:
- `GET /api/achievements/` - List all achievements
- `GET /api/achievements/my_achievements/` - Your achievements
- `POST /api/user_goals/` - Create new goal
- `GET /api/user_goals/` - Your goals

## 🐛 Troubleshooting

### "Cannot connect to server"
- Verifică dacă backend-ul rulează pe port 8000
- Verifică dacă frontend-ul rulează pe port 5173
- Verifică CORS settings în backend

### "Invalid credentials"
- Folosește exact credențialele de mai sus
- Username: `testuser` (lowercase)
- Password: `test123`

### "Token expired"
- Fă login din nou pentru un token nou
- Sau folosește refresh token endpoint

### Server nu pornește
- Verifică dacă ai toate dependențele instalate:
  ```bash
  pip install -r requirements.txt
  ```
- Verifică dacă migrations sunt aplicate:
  ```bash
  python manage.py migrate
  ```

## 🎯 Next Steps

1. **Test Login** - Loghează-te cu `testuser/test123`
2. **Test API** - Încearcă endpoint-urile cu Postman
3. **Update Frontend** - Integrează noile API endpoints
4. **Create More Users** - Register new users pentru testare

## 📚 Documentație Completă

Vezi **IMPLEMENTATION_BACKEND.md** pentru:
- Lista completă de endpoints
- Exemple de request/response
- Cod pentru frontend
- Detalii despre automatic progress tracking

## ✨ Features Implementate

✅ Avatar upload
✅ Profile editing (bio, city, phone)
✅ Private sessions
✅ Join/Leave sessions
✅ Chat (private + group)
✅ Automatic progress tracking (streak, goals, achievements)
✅ User search
✅ Block/unblock users
✅ Session filters and sorting
✅ History
✅ Rating with feedback

---

**Backend Status: ✅ READY**
**Frontend Status: 🔄 Needs Integration**

Happy coding! 🚀
