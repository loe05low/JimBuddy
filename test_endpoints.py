#!/usr/bin/env python3
"""
Script pentru testarea manuală a tuturor endpoint-urilor SpotMe API
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_test(test_name):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}TEST: {test_name}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

def print_success(message):
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    print(f"{RED}✗ {message}{RESET}")

def print_info(message):
    print(f"{YELLOW}ℹ {message}{RESET}")

def print_response(response):
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")

# Store test data
test_data = {
    'user1_token': None,
    'user2_token': None,
    'user1_id': None,
    'user2_id': None,
    'gym_id': None,
    'session_id': None,
    'request_id': None
}

# TEST 1: REGISTER USER 1
print_test("1. Register User 1 (testuser)")
try:
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "username": "testuser_manual",
        "email": "testuser@manual.com",
        "password": "test123",
        "password_confirm": "test123",
        "nume": "Test User Manual",
        "grad": "Intermediar"
    })
    print_response(response)
    if response.status_code == 201:
        data = response.json()
        test_data['user1_token'] = data.get('access')
        test_data['user1_id'] = data.get('user', {}).get('id')
        print_success(f"User 1 registered successfully! Token: {test_data['user1_token'][:20]}...")
    else:
        print_error("Registration failed!")
except Exception as e:
    print_error(f"Error: {str(e)}")

# TEST 2: REGISTER USER 2
print_test("2. Register User 2 (gymbuddy)")
try:
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "username": "gymbuddy_manual",
        "email": "gymbuddy@manual.com",
        "password": "buddy123",
        "password_confirm": "buddy123",
        "nume": "Gym Buddy Manual",
        "grad": "Avansat"
    })
    print_response(response)
    if response.status_code == 201:
        data = response.json()
        test_data['user2_token'] = data.get('access')
        test_data['user2_id'] = data.get('user', {}).get('id')
        print_success(f"User 2 registered successfully! Token: {test_data['user2_token'][:20]}...")
    else:
        print_error("Registration failed!")
except Exception as e:
    print_error(f"Error: {str(e)}")

# TEST 3: LOGIN USER 1
print_test("3. Login User 1")
try:
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": "testuser_manual",
        "password": "test123"
    })
    print_response(response)
    if response.status_code == 200:
        data = response.json()
        test_data['user1_token'] = data.get('access')
        print_success(f"Login successful! New token: {test_data['user1_token'][:20]}...")
    else:
        print_error("Login failed!")
except Exception as e:
    print_error(f"Error: {str(e)}")

# TEST 4: GET CURRENT USER
print_test("4. Get Current User Info")
try:
    headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print_response(response)
    if response.status_code == 200:
        print_success("Current user info retrieved successfully!")
    else:
        print_error("Failed to get current user!")
except Exception as e:
    print_error(f"Error: {str(e)}")

# TEST 5: GET GYMS LIST
print_test("5. Get Gyms List (PUBLIC)")
try:
    response = requests.get(f"{BASE_URL}/sali/")
    print_response(response)
    if response.status_code == 200:
        gyms = response.json()
        if len(gyms) > 0:
            test_data['gym_id'] = gyms[0]['id']
            print_success(f"Found {len(gyms)} gyms! Using gym: {gyms[0]['nume']}")
        else:
            print_error("No gyms found! Run: python manage.py populate_demo_gyms")
    else:
        print_error("Failed to get gyms!")
except Exception as e:
    print_error(f"Error: {str(e)}")

# TEST 6: GET SINGLE GYM
if test_data['gym_id']:
    print_test("6. Get Single Gym Details")
    try:
        response = requests.get(f"{BASE_URL}/sali/{test_data['gym_id']}/")
        print_response(response)
        if response.status_code == 200:
            print_success("Gym details retrieved successfully!")
        else:
            print_error("Failed to get gym details!")
    except Exception as e:
        print_error(f"Error: {str(e)}")

# TEST 7: CREATE SESSION (User 1)
if test_data['gym_id'] and test_data['user1_token']:
    print_test("7. Create Workout Session (User 1)")
    try:
        headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
        expiration_time = (datetime.now() + timedelta(days=1)).isoformat()
        response = requests.post(f"{BASE_URL}/sesiuni/",
            headers=headers,
            json={
                "sala": test_data['gym_id'],
                "tip_antrenament": "Strength Training",
                "interval_orar": "18:00 - 20:00",
                "descriere": "Focus pe chest and arms - manual test",
                "data_expirare": expiration_time
            })
        print_response(response)
        if response.status_code == 201:
            data = response.json()
            test_data['session_id'] = data.get('id')
            print_success(f"Session created! ID: {test_data['session_id']}")
        else:
            print_error("Failed to create session!")
    except Exception as e:
        print_error(f"Error: {str(e)}")

# TEST 8: GET ALL SESSIONS
print_test("8. Get All Sessions (PUBLIC)")
try:
    response = requests.get(f"{BASE_URL}/sesiuni/")
    print_response(response)
    if response.status_code == 200:
        sessions = response.json()
        print_success(f"Found {len(sessions)} sessions!")
    else:
        print_error("Failed to get sessions!")
except Exception as e:
    print_error(f"Error: {str(e)}")

# TEST 9: GET ACTIVE SESSIONS ONLY
print_test("9. Get Active Sessions Only (Filter)")
try:
    response = requests.get(f"{BASE_URL}/sesiuni/?status=activ")
    print_response(response)
    if response.status_code == 200:
        sessions = response.json()
        print_success(f"Found {len(sessions)} active sessions!")
    else:
        print_error("Failed to get active sessions!")
except Exception as e:
    print_error(f"Error: {str(e)}")

# TEST 10: GET SINGLE SESSION
if test_data['session_id']:
    print_test("10. Get Single Session Details")
    try:
        response = requests.get(f"{BASE_URL}/sesiuni/{test_data['session_id']}/")
        print_response(response)
        if response.status_code == 200:
            print_success("Session details retrieved successfully!")
        else:
            print_error("Failed to get session details!")
    except Exception as e:
        print_error(f"Error: {str(e)}")

# TEST 11: SEND BUDDY REQUEST (User 2 -> Session of User 1)
if test_data['session_id'] and test_data['user2_token']:
    print_test("11. Send Buddy Request (User 2 -> User 1's Session)")
    try:
        headers = {'Authorization': f'Bearer {test_data["user2_token"]}'}
        response = requests.post(f"{BASE_URL}/cereri/",
            headers=headers,
            json={
                "sesiune": test_data['session_id'],
                "mesaj": "Hey! I'd like to join your workout session. Manual test request."
            })
        print_response(response)
        if response.status_code == 201:
            data = response.json()
            test_data['request_id'] = data.get('id')
            print_success(f"Buddy request sent! ID: {test_data['request_id']}")
        else:
            print_error("Failed to send buddy request!")
    except Exception as e:
        print_error(f"Error: {str(e)}")

# TEST 12: GET MY SENT REQUESTS (User 2)
if test_data['user2_token']:
    print_test("12. Get My Sent Requests (User 2)")
    try:
        headers = {'Authorization': f'Bearer {test_data["user2_token"]}'}
        response = requests.get(f"{BASE_URL}/cereri/my_sent_requests/", headers=headers)
        print_response(response)
        if response.status_code == 200:
            print_success("Sent requests retrieved successfully!")
        else:
            print_error("Failed to get sent requests!")
    except Exception as e:
        print_error(f"Error: {str(e)}")

# TEST 13: GET RECEIVED REQUESTS (User 1)
if test_data['user1_token']:
    print_test("13. Get Received Requests (User 1)")
    try:
        headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
        response = requests.get(f"{BASE_URL}/cereri/my_received_requests/", headers=headers)
        print_response(response)
        if response.status_code == 200:
            print_success("Received requests retrieved successfully!")
        else:
            print_error("Failed to get received requests!")
    except Exception as e:
        print_error(f"Error: {str(e)}")

# TEST 14: ACCEPT BUDDY REQUEST (User 1 accepts User 2's request)
if test_data['request_id'] and test_data['user1_token']:
    print_test("14. Accept Buddy Request (User 1 accepts)")
    try:
        headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
        response = requests.patch(f"{BASE_URL}/cereri/{test_data['request_id']}/accept_request/",
            headers=headers)
        print_response(response)
        if response.status_code == 200:
            print_success("Buddy request accepted!")
        else:
            print_error("Failed to accept buddy request!")
    except Exception as e:
        print_error(f"Error: {str(e)}")

# TEST 15: GET MY PROFILE (User 1)
if test_data['user1_token']:
    print_test("15. Get My Profile (User 1)")
    try:
        headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
        response = requests.get(f"{BASE_URL}/profiles/me/", headers=headers)
        print_response(response)
        if response.status_code == 200:
            print_success("Profile retrieved successfully!")
        else:
            print_error("Failed to get profile!")
    except Exception as e:
        print_error(f"Error: {str(e)}")

# TEST 16: GET USER PROFILE BY ID (User 2's profile)
if test_data['user2_id']:
    print_test(f"16. Get User Profile by ID (User 2 - ID: {test_data['user2_id']})")
    try:
        response = requests.get(f"{BASE_URL}/profiles/{test_data['user2_id']}/")
        print_response(response)
        if response.status_code == 200:
            print_success("User profile retrieved successfully!")
        else:
            print_error("Failed to get user profile!")
    except Exception as e:
        print_error(f"Error: {str(e)}")

# TEST 17: CREATE RATING (User 1 rates User 2)
if test_data['user1_token'] and test_data['user2_id']:
    print_test("17. Create Rating (User 1 rates User 2)")
    try:
        headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
        response = requests.post(f"{BASE_URL}/rating/",
            headers=headers,
            json={
                "user_primit": test_data['user2_id'],
                "nota": 5,
                "comentariu": "Great workout buddy! Very motivated and helpful. Manual test rating."
            })
        print_response(response)
        if response.status_code == 201:
            print_success("Rating created successfully!")
        else:
            print_error("Failed to create rating!")
    except Exception as e:
        print_error(f"Error: {str(e)}")

# TEST 18: GET USER RATINGS (User 2's ratings)
if test_data['user2_id']:
    print_test(f"18. Get User Ratings (User 2 - ID: {test_data['user2_id']})")
    try:
        response = requests.get(f"{BASE_URL}/profiles/{test_data['user2_id']}/ratings/")
        print_response(response)
        if response.status_code == 200:
            print_success("User ratings retrieved successfully!")
        else:
            print_error("Failed to get user ratings!")
    except Exception as e:
        print_error(f"Error: {str(e)}")

# TEST 19: UPDATE SESSION (User 1 updates their session)
if test_data['session_id'] and test_data['user1_token']:
    print_test("19. Update Session (User 1)")
    try:
        headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
        response = requests.patch(f"{BASE_URL}/sesiuni/{test_data['session_id']}/",
            headers=headers,
            json={
                "tip_antrenament": "Full Body Workout",
                "descriere": "Changed to full body workout - manual test update"
            })
        print_response(response)
        if response.status_code == 200:
            print_success("Session updated successfully!")
        else:
            print_error("Failed to update session!")
    except Exception as e:
        print_error(f"Error: {str(e)}")

# TEST 20: ARCHIVE SESSION (User 1 archives their session)
if test_data['session_id'] and test_data['user1_token']:
    print_test("20. Archive Session (User 1)")
    try:
        headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
        response = requests.patch(f"{BASE_URL}/sesiuni/{test_data['session_id']}/",
            headers=headers,
            json={
                "status": "arhivat"
            })
        print_response(response)
        if response.status_code == 200:
            print_success("Session archived successfully!")
        else:
            print_error("Failed to archive session!")
    except Exception as e:
        print_error(f"Error: {str(e)}")

# FINAL SUMMARY
print(f"\n{BLUE}{'='*60}{RESET}")
print(f"{BLUE}SUMMARY - Test Data Collected:{RESET}")
print(f"{BLUE}{'='*60}{RESET}")
print(f"User 1 ID: {test_data['user1_id']}")
print(f"User 1 Token: {test_data['user1_token'][:30] if test_data['user1_token'] else 'N/A'}...")
print(f"User 2 ID: {test_data['user2_id']}")
print(f"User 2 Token: {test_data['user2_token'][:30] if test_data['user2_token'] else 'N/A'}...")
print(f"Gym ID: {test_data['gym_id']}")
print(f"Session ID: {test_data['session_id']}")
print(f"Request ID: {test_data['request_id']}")
print(f"{BLUE}{'='*60}{RESET}\n")

print(f"{GREEN}✓ All endpoint tests completed!{RESET}")
