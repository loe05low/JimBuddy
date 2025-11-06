# Rating & Progress Tracking - Test Guide

## 🎯 Features Implemented

### 1. Rating System
- **Star Rating**: 1-5 stars with hover effects
- **Comments**: Optional text feedback
- **Automatic Updates**: Rating average and workout count auto-update

### 2. Progress Tracking
- **Total Workouts**: Number of completed sessions
- **Average Rating**: Overall rating from all gym buddies
- **Fitness Level**: Current fitness grade

## 📋 How to Test

### Prerequisites
1. Start PostgreSQL database
2. Start Django backend: `python manage.py runserver`
3. Start React frontend: `npm start`
4. Have 2 user accounts (for rating each other)

### Test Scenario 1: View Progress Stats
1. Login to your account
2. Go to Profile page
3. ✅ Verify you see 3 colorful cards:
   - **Purple card**: Total Workouts count
   - **Yellow card**: Average Rating with stars
   - **Pink card**: Fitness Level

### Test Scenario 2: Give Rating to Past Session
1. Login as User A
2. Go to Home (Map view)
3. Find a session created by User B that has expired (data_expirare < now)
4. Click on the session marker
5. ✅ Verify you see "⭐ Rate Your Gym Buddy" button (yellow/orange)
6. Click the rating button
7. ✅ Verify Rating Modal appears with:
   - Session owner name
   - 5 star rating buttons
   - Comment text area
   - Submit and Cancel buttons

### Test Scenario 3: Submit Rating
1. In the Rating Modal, click on stars (1-5)
2. ✅ Verify stars light up yellow when clicked
3. ✅ Verify label shows (Poor/Fair/Good/Very Good/Excellent)
4. Type a comment (optional)
5. Click "Submit Rating"
6. ✅ Verify success message appears
7. ✅ Verify modal closes after 2 seconds

### Test Scenario 4: Check Rating Updates
1. Login as User B (the person who received the rating)
2. Go to Profile page
3. ✅ Verify "Total Workouts" increased by 1
4. ✅ Verify "Average Rating" updated
5. Click on "Ratings" tab
6. ✅ Verify you see the new rating with:
   - User A's name
   - Star rating
   - Comment (if provided)
   - Date

### Test Scenario 5: Check Rating Giver's Stats
1. Login as User A (the person who gave the rating)
2. Go to Profile page
3. ✅ Verify "Total Workouts" increased by 1
4. Note: Only people who RECEIVE ratings see them in the Ratings tab

## 🔧 API Endpoints Used

```
POST /api/rating/
Body:
{
  "to_user": "uuid-of-user",
  "sesiune": "uuid-of-session",
  "rating": 4.5,
  "comentariu": "Optional comment"
}

GET /api/rating/
Response: List of all ratings

GET /api/profiles/me/
Response: User profile with rating, nr_antrenamente, grad
```

## 🐛 Troubleshooting

### Rating button doesn't appear
- Check if session is expired (data_expirare < now)
- Make sure you're not the session owner
- Refresh the page

### Rating not saving
- Check browser console for errors
- Verify backend is running
- Check if you already rated this session (duplicate error)

### Stats not updating
- Refresh the Profile page
- Check backend logs for errors
- Verify rating was saved successfully

## 📊 Database Models

### Rating Model
- from_user: Who gave the rating
- to_user: Who received the rating
- sesiune: Which session
- rating: 1.0 - 5.0 (decimal)
- comentariu: Text (optional)
- data: Auto timestamp

### UserProfile Updates
- rating: Auto-calculated average
- nr_antrenamente: Auto-incremented for both users
- grad: Manual or auto-progression

## ✅ Success Criteria

All features working if:
- ✅ Can give rating to expired sessions
- ✅ Star rating works with hover effects
- ✅ Rating saves to database
- ✅ Profile stats update automatically
- ✅ Workout count increments for both users
- ✅ Average rating recalculates correctly
- ✅ Ratings appear in Profile → Ratings tab
- ✅ Cannot rate your own sessions
- ✅ Cannot rate active (non-expired) sessions
