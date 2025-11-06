# 🧪 SpotMe - Testing Guide

Ghid complet pentru testarea aplicației SpotMe (Gym Buddy Finder).

---

## 📋 Prerequisites

Asigură-te că ai instalat:
- **Python 3.11+**
- **Node.js 18+**
- **npm** sau **yarn**

---

## 🚀 Quick Start - Rulare Aplicație

### 1. Backend Django (Terminal 1)

```bash
# Navigate to backend
cd backend

# Install dependencies (first time only)
pip install -r requirements.txt

# Run migrations (first time only)
python manage.py migrate

# Create superuser for admin (first time only)
python manage.py createsuperuser
# Username: admin
# Password: admin123

# Populate demo gyms (first time only)
python manage.py populate_demo_gyms

# Start Django server
python manage.py runserver
```

**Backend running at:** `http://localhost:8000`
**Admin Panel:** `http://localhost:8000/admin` (admin/admin123)

---

### 2. Frontend React (Terminal 2)

```bash
# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

**Frontend running at:** `http://localhost:5173`

---

## 🧪 Testing Scenarios

### Scenario 1: User Registration & Login

1. **Register New User**
   - Open `http://localhost:5173`
   - Click "Register here"
   - Fill form:
     - Username: `testuser`
     - Email: `test@test.com`
     - Full Name: `Test User`
     - Experience Level: `Intermediar`
     - Password: `test123`
     - Confirm Password: `test123`
   - Click "Register"
   - ✅ **Expected:** Redirect to home page with map

2. **Logout & Login**
   - Click "Logout" in navbar
   - ✅ **Expected:** Redirect to login page
   - Enter credentials: `testuser` / `test123`
   - Click "Login"
   - ✅ **Expected:** Redirect to home with map

---

### Scenario 2: Create Workout Session

1. **View Map with Gyms**
   - ✅ **Expected:** Map centered on București
   - ✅ **Expected:** 8 gym markers (dumbbell icons) visible

2. **Create Session at Gym**
   - Click on any gym marker (e.g., "World Class Victoriei")
   - Click "Create Session Here" in popup
   - Fill form:
     - Workout Type: `Strength Training`
     - Time Slot: `18:00 - 20:00`
     - Description: `Focus on chest and arms`
     - Expires At: (tomorrow at 20:00)
   - Click "Create Session"
   - ✅ **Expected:** Modal closes, session appears on map with different icon

3. **View Session on Map**
   - ✅ **Expected:** New marker appears at the gym location
   - Click session marker
   - ✅ **Expected:** Popup shows session details:
     - User name, experience level, rating
     - Workout type, time slot
     - "View Details" button

---

### Scenario 3: Send & Manage Buddy Requests

**Setup:** Create 2nd user to test requests

1. **Logout and Register 2nd User**
   - Logout from `testuser`
   - Register new user: `gymbuddy` / `buddy123`

2. **View Active Sessions**
   - ✅ **Expected:** See session created by `testuser`
   - Click on session marker
   - Click "View Details"
   - ✅ **Expected:** See full session details + user profile info

3. **Send Buddy Request**
   - Click "Send Buddy Request"
   - ✅ **Expected:** Success message "Request sent successfully!"
   - ✅ **Expected:** Modal closes

4. **Check Sent Requests**
   - Go to Profile page (click username in navbar)
   - Click "Requests" tab
   - Scroll to "My Sent Requests"
   - ✅ **Expected:** See request with "Pending" badge

5. **Accept Request (as session owner)**
   - Logout and login as `testuser` (session owner)
   - Go to Profile → Requests tab
   - ✅ **Expected:** See "Requests Received" with `gymbuddy`'s request
   - Click "Accept"
   - ✅ **Expected:** Request disappears from pending list

6. **Verify Acceptance (as requester)**
   - Logout and login as `gymbuddy`
   - Go to Profile → Requests → My Sent Requests
   - ✅ **Expected:** Request status changed to "Accepted" (green badge)

---

### Scenario 4: Rating System

**Note:** Ratings are given after workout completion

1. **Give Rating**
   - Login as `testuser`
   - Navigate to Profile
   - _(Simulating post-workout rating)_
   - Use API directly or wait for frontend rating form implementation

2. **View Ratings**
   - Go to Profile → Ratings tab
   - ✅ **Expected:** See received ratings ordered by date (newest first)
   - Each rating shows:
     - From user name & experience level
     - Star rating (1-5)
     - Optional comment
     - Date

---

### Scenario 5: Admin Panel Management

1. **Access Admin Panel**
   - Open `http://localhost:8000/admin`
   - Login: `admin` / `admin123`

2. **Manage Gyms**
   - Click "Săli de Fitness"
   - ✅ **Expected:** See 8 demo gyms
   - Click "Add Sala de Fitness"
   - Add new gym with coordinates
   - ✅ **Expected:** New gym appears on frontend map (refresh page)

3. **Manage Users**
   - Click "Users"
   - ✅ **Expected:** See all registered users with ratings
   - Click user to view/edit profile

4. **View Sessions**
   - Click "Sesiuni de Antrenament"
   - ✅ **Expected:** See all sessions with status
   - Select sessions → Actions → "Arhivează sesiunile selectate"
   - ✅ **Expected:** Sessions status changes to "arhivat"

5. **View Requests**
   - Click "Cereri Gym Buddy"
   - ✅ **Expected:** See all buddy requests with status

---

## 🔍 API Testing (Optional)

### Using cURL

**1. Register User**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "apiuser",
    "email": "api@test.com",
    "password": "api123",
    "password_confirm": "api123",
    "nume": "API User",
    "grad": "Avansat"
  }'
```

**2. Login & Get Token**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "apiuser",
    "password": "api123"
  }'
# Copy the "access" token
```

**3. Get Gyms List**
```bash
curl http://localhost:8000/api/sali/
```

**4. Create Session (with auth)**
```bash
curl -X POST http://localhost:8000/api/sesiuni \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "sala": "SALA_UUID_FROM_GYMS_LIST",
    "tip_antrenament": "Cardio",
    "interval_orar": "19:00 - 21:00",
    "descriere": "High intensity cardio session",
    "data_expirare": "2025-11-08T21:00:00Z"
  }'
```

**5. Get My Profile**
```bash
curl http://localhost:8000/api/profiles/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## ✅ Feature Checklist

### Backend
- [x] User registration with profile
- [x] JWT authentication (login/refresh)
- [x] 8 demo gyms in București
- [x] CRUD operations for sessions
- [x] Buddy request system (send/accept/reject)
- [x] Rating system with comments
- [x] Admin panel for gyms/users management
- [x] Auto-archiving expired sessions (cron job)
- [x] Profile with rating/stats calculation

### Frontend
- [x] Login/Register pages with validation
- [x] JWT token management (auto-refresh)
- [x] Protected routes
- [x] Interactive map with OpenStreetMap
- [x] Gym markers (8 locations)
- [x] Session markers (active sessions)
- [x] Session creation form (modal)
- [x] Session details view (modal)
- [x] Buddy request sending
- [x] Request management (accept/reject)
- [x] User profile page
- [x] Ratings & comments display
- [x] Responsive design (mobile/desktop)
- [x] Real-time data updates

---

## 🐛 Common Issues & Solutions

### Issue 1: Backend won't start
**Error:** `ModuleNotFoundError: No module named 'rest_framework'`
**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### Issue 2: Database not found
**Error:** `no such table: users_userprofile`
**Solution:**
```bash
python manage.py migrate
```

### Issue 3: Frontend build fails
**Error:** `Cannot find module 'tailwindcss'`
**Solution:**
```bash
cd frontend
npm install
```

### Issue 4: Map not loading
**Error:** Blank map area
**Solution:**
- Check browser console for errors
- Verify backend is running at `http://localhost:8000`
- Check that gyms exist: `curl http://localhost:8000/api/sali/`

### Issue 5: CORS errors
**Error:** `Access-Control-Allow-Origin`
**Solution:**
- Ensure frontend `.env` has `VITE_API_URL=http://localhost:8000/api`
- Restart both servers

---

## 📊 Expected Data

### Demo Gyms (8 locations in București)
1. World Class Victoriei
2. GymBox Obor
3. Iron Gym Militari
4. Gold's Gym Universitate
5. FitLife Unirii
6. CrossFit Arena Pipera
7. PowerGym Timpuri Noi
8. Body & Mind Fitness Herastrau

### User Profile Fields
- Username
- Email
- Full Name (nume)
- Experience Level (grad): Începător → Veteran
- Rating (1-5 stars, default 5.0)
- Total Workouts (nr_antrenamente)

### Session Status
- `activ` - Currently available
- `expirat` - Past expiration time
- `arhivat` - Archived (not shown on map)

### Request Status
- `pending` - Waiting for owner response
- `acceptat` - Approved by owner
- `refuzat` - Rejected by owner

---

## 🎯 Success Criteria

Application is working correctly if:
1. ✅ Users can register and login
2. ✅ Map displays 8 gym markers
3. ✅ Users can create workout sessions
4. ✅ Sessions appear on map with different markers
5. ✅ Users can send buddy requests
6. ✅ Session owners can accept/reject requests
7. ✅ Ratings display on user profiles
8. ✅ Admin can manage gyms and users
9. ✅ No console errors in browser
10. ✅ Responsive on mobile and desktop

---

## 📞 Support

For issues or questions:
- Check browser console for errors (F12)
- Check backend terminal for Django errors
- Review `README.md` for detailed API documentation
- Test API endpoints directly with cURL

---

**Happy Testing! 💪🏋️**
