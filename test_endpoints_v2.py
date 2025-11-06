#!/usr/bin/env python3
"""
Script comprehensive pentru testarea tuturor endpoint-urilor SpotMe API
Versiunea 2 - cu useri existenți
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_test(test_name):
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}✦ {test_name}{RESET}")
    print(f"{BLUE}{'='*70}{RESET}")

def print_success(message):
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    print(f"{RED}✗ {message}{RESET}")

def print_info(message):
    print(f"{YELLOW}ℹ {message}{RESET}")

def print_response(response, show_full=False):
    print(f"Status: {response.status_code} ", end='')
    if response.status_code == 200:
        print(GREEN + "OK" + RESET)
    elif response.status_code == 201:
        print(GREEN + "CREATED" + RESET)
    elif response.status_code == 204:
        print(GREEN + "NO CONTENT" + RESET)
    elif response.status_code >= 400:
        print(RED + "ERROR" + RESET)
    else:
        print(YELLOW + "..." + RESET)

    if show_full:
        try:
            data = response.json()
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except:
            print(response.text)

# Test data storage
test_data = {
    'user1_token': None,
    'user2_token': None,
    'user1_id': None,
    'user2_id': None,
    'gym_id': None,
    'session_id': None,
    'request_id': None
}

results = {
    'passed': 0,
    'failed': 0,
    'total': 0
}

def test_endpoint(test_name, func):
    """Helper to run a test and track results"""
    results['total'] += 1
    print_test(f"{results['total']}. {test_name}")
    try:
        success = func()
        if success:
            results['passed'] += 1
            print_success("PASSED")
        else:
            results['failed'] += 1
            print_error("FAILED")
        return success
    except Exception as e:
        results['failed'] += 1
        print_error(f"EXCEPTION: {str(e)}")
        return False

# ============================================================================
# TEST FUNCTIONS
# ============================================================================

def test_register_or_login_user1():
    """Register or login user 1"""
    # Try register first
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "username": "testuser_v2",
        "email": "testv2@test.com",
        "password": "test123",
        "password_confirm": "test123",
        "nume": "Test User V2",
        "grad": "Intermediar"
    })
    print_response(response)

    if response.status_code == 201:
        data = response.json()
        test_data['user1_token'] = data.get('tokens', {}).get('access')
        test_data['user1_id'] = data.get('user', {}).get('id')
        print_info(f"New user created! ID: {test_data['user1_id']}")
        return True
    else:
        # User exists, login instead
        print_info("User exists, logging in...")
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "username": "testuser_v2",
            "password": "test123"
        })
        print_response(response)
        if response.status_code == 200:
            data = response.json()
            test_data['user1_token'] = data.get('access')
            # Get user ID from /me endpoint
            headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
            me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
            if me_response.status_code == 200:
                test_data['user1_id'] = me_response.json().get('id')
                print_info(f"Logged in! ID: {test_data['user1_id']}")
            return True
    return False

def test_register_or_login_user2():
    """Register or login user 2"""
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "username": "gymbuddy_v2",
        "email": "buddyv2@test.com",
        "password": "buddy123",
        "password_confirm": "buddy123",
        "nume": "Gym Buddy V2",
        "grad": "Avansat"
    })
    print_response(response)

    if response.status_code == 201:
        data = response.json()
        test_data['user2_token'] = data.get('tokens', {}).get('access')
        test_data['user2_id'] = data.get('user', {}).get('id')
        print_info(f"New user created! ID: {test_data['user2_id']}")
        return True
    else:
        print_info("User exists, logging in...")
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "username": "gymbuddy_v2",
            "password": "buddy123"
        })
        print_response(response)
        if response.status_code == 200:
            data = response.json()
            test_data['user2_token'] = data.get('access')
            headers = {'Authorization': f'Bearer {test_data["user2_token"]}'}
            me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
            if me_response.status_code == 200:
                test_data['user2_id'] = me_response.json().get('id')
                print_info(f"Logged in! ID: {test_data['user2_id']}")
            return True
    return False

def test_get_current_user():
    """Get current user info"""
    headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print_response(response)
    return response.status_code == 200

def test_get_gyms():
    """Get all gyms (public endpoint)"""
    response = requests.get(f"{BASE_URL}/sali/")
    print_response(response)
    if response.status_code == 200:
        gyms = response.json().get('results', [])
        if len(gyms) > 0:
            test_data['gym_id'] = gyms[0]['id']
            print_info(f"Found {len(gyms)} gyms. Using: {gyms[0]['nume']}")
            return True
        else:
            print_error("No gyms found! Run: python manage.py populate_demo_gyms")
    return False

def test_get_single_gym():
    """Get single gym details"""
    if not test_data['gym_id']:
        print_error("No gym ID available")
        return False
    response = requests.get(f"{BASE_URL}/sali/{test_data['gym_id']}/")
    print_response(response, show_full=True)
    return response.status_code == 200

def test_create_session():
    """Create workout session (authenticated)"""
    if not test_data['gym_id'] or not test_data['user1_token']:
        print_error("Missing prerequisites")
        return False

    headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
    expiration = (datetime.now() + timedelta(days=1)).isoformat()
    response = requests.post(f"{BASE_URL}/sesiuni/",
        headers=headers,
        json={
            "sala": test_data['gym_id'],
            "tip_antrenament": "Strength Training",
            "interval_orar": "18:00 - 20:00",
            "descriere": "Chest and arms workout - V2 test",
            "data_expirare": expiration
        })
    print_response(response, show_full=True)
    if response.status_code == 201:
        test_data['session_id'] = response.json().get('id')
        print_info(f"Session created! ID: {test_data['session_id']}")
        return True
    return False

def test_get_all_sessions():
    """Get all sessions (authenticated)"""
    headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
    response = requests.get(f"{BASE_URL}/sesiuni/", headers=headers)
    print_response(response)
    if response.status_code == 200:
        sessions = response.json()
        count = sessions.get('count', len(sessions)) if isinstance(sessions, dict) else len(sessions)
        print_info(f"Found {count} sessions")
        return True
    return False

def test_get_active_sessions():
    """Get active sessions only"""
    headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
    response = requests.get(f"{BASE_URL}/sesiuni/?status=activ", headers=headers)
    print_response(response)
    if response.status_code == 200:
        sessions = response.json()
        count = sessions.get('count', len(sessions)) if isinstance(sessions, dict) else len(sessions)
        print_info(f"Found {count} active sessions")
        return True
    return False

def test_get_single_session():
    """Get single session details"""
    if not test_data['session_id']:
        print_error("No session ID available")
        return False
    headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
    response = requests.get(f"{BASE_URL}/sesiuni/{test_data['session_id']}/", headers=headers)
    print_response(response, show_full=True)
    return response.status_code == 200

def test_send_buddy_request():
    """Send buddy request (user 2 -> user 1's session)"""
    if not test_data['session_id'] or not test_data['user2_token']:
        print_error("Missing prerequisites")
        return False

    headers = {'Authorization': f'Bearer {test_data["user2_token"]}'}
    response = requests.post(f"{BASE_URL}/cereri/",
        headers=headers,
        json={
            "sesiune": test_data['session_id']
        })
    print_response(response, show_full=True)
    if response.status_code == 201:
        test_data['request_id'] = response.json().get('id')
        print_info(f"Request sent! ID: {test_data['request_id']}")
        return True
    return False

def test_get_sent_requests():
    """Get my sent requests (user 2)"""
    headers = {'Authorization': f'Bearer {test_data["user2_token"]}'}
    response = requests.get(f"{BASE_URL}/cereri/my_sent_requests/", headers=headers)
    print_response(response, show_full=True)
    return response.status_code == 200

def test_get_received_requests():
    """Get received requests (user 1)"""
    headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
    response = requests.get(f"{BASE_URL}/cereri/my_received_requests/", headers=headers)
    print_response(response, show_full=True)
    return response.status_code == 200

def test_accept_buddy_request():
    """Accept buddy request (user 1 accepts)"""
    if not test_data['request_id'] or not test_data['user1_token']:
        print_error("Missing prerequisites")
        return False

    headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
    response = requests.patch(
        f"{BASE_URL}/cereri/{test_data['request_id']}/accept_request/",
        headers=headers)
    print_response(response, show_full=True)
    return response.status_code == 200

def test_get_my_profile():
    """Get my profile (user 1)"""
    headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
    response = requests.get(f"{BASE_URL}/profiles/me/", headers=headers)
    print_response(response, show_full=True)
    return response.status_code == 200

def test_get_user_profile():
    """Get user profile by ID (user 2's profile)"""
    if not test_data['user2_id']:
        print_error("No user 2 ID available")
        return False
    response = requests.get(f"{BASE_URL}/profiles/{test_data['user2_id']}/")
    print_response(response, show_full=True)
    return response.status_code == 200

def test_create_rating():
    """Create rating (user 1 rates user 2)"""
    if not test_data['user1_token'] or not test_data['user2_id'] or not test_data['session_id']:
        print_error("Missing prerequisites")
        return False

    headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
    response = requests.post(f"{BASE_URL}/rating/",
        headers=headers,
        json={
            "to_user": test_data['user2_id'],
            "sesiune": test_data['session_id'],
            "rating": 5.0,
            "comentariu": "Excellent workout partner! V2 test rating."
        })
    print_response(response, show_full=True)
    return response.status_code == 201

def test_get_user_ratings():
    """Get user ratings (user 2's ratings)"""
    if not test_data['user2_id']:
        print_error("No user 2 ID available")
        return False
    response = requests.get(f"{BASE_URL}/profiles/{test_data['user2_id']}/ratings/")
    print_response(response, show_full=True)
    return response.status_code == 200

def test_update_session():
    """Update session (user 1 updates their session)"""
    if not test_data['session_id'] or not test_data['user1_token']:
        print_error("Missing prerequisites")
        return False

    headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
    response = requests.patch(f"{BASE_URL}/sesiuni/{test_data['session_id']}/",
        headers=headers,
        json={
            "tip_antrenament": "Full Body Workout",
            "descriere": "Changed to full body - V2 test update"
        })
    print_response(response, show_full=True)
    return response.status_code == 200

# ============================================================================
# RUN ALL TESTS
# ============================================================================

print(f"\n{BLUE}{'='*70}{RESET}")
print(f"{BLUE}   SPOTME API - COMPREHENSIVE ENDPOINT TESTING V2{RESET}")
print(f"{BLUE}{'='*70}{RESET}\n")

# Authentication Tests
test_endpoint("Register/Login User 1 (testuser_v2)", test_register_or_login_user1)
test_endpoint("Register/Login User 2 (gymbuddy_v2)", test_register_or_login_user2)
test_endpoint("Get Current User Info", test_get_current_user)

# Gym Tests
test_endpoint("Get All Gyms (PUBLIC)", test_get_gyms)
test_endpoint("Get Single Gym Details", test_get_single_gym)

# Session Tests
test_endpoint("Create Workout Session (User 1)", test_create_session)
test_endpoint("Get All Sessions", test_get_all_sessions)
test_endpoint("Get Active Sessions Only", test_get_active_sessions)
test_endpoint("Get Single Session Details", test_get_single_session)

# Buddy Request Tests
test_endpoint("Send Buddy Request (User 2 -> User 1)", test_send_buddy_request)
test_endpoint("Get My Sent Requests (User 2)", test_get_sent_requests)
test_endpoint("Get Received Requests (User 1)", test_get_received_requests)
test_endpoint("Accept Buddy Request (User 1)", test_accept_buddy_request)

# Profile Tests
test_endpoint("Get My Profile (User 1)", test_get_my_profile)
test_endpoint("Get User Profile by ID (User 2)", test_get_user_profile)

# Rating Tests
test_endpoint("Create Rating (User 1 -> User 2)", test_create_rating)
test_endpoint("Get User Ratings (User 2)", test_get_user_ratings)

# Update Tests
test_endpoint("Update Session (User 1)", test_update_session)

# ============================================================================
# FINAL RESULTS
# ============================================================================

print(f"\n{BLUE}{'='*70}{RESET}")
print(f"{BLUE}   FINAL RESULTS{RESET}")
print(f"{BLUE}{'='*70}{RESET}\n")

print(f"Total Tests: {results['total']}")
print(f"{GREEN}Passed: {results['passed']}{RESET}")
print(f"{RED}Failed: {results['failed']}{RESET}")

success_rate = (results['passed'] / results['total'] * 100) if results['total'] > 0 else 0
print(f"\nSuccess Rate: {success_rate:.1f}%")

if results['failed'] == 0:
    print(f"\n{GREEN}{'🎉 '*10}{RESET}")
    print(f"{GREEN}  ALL TESTS PASSED! API is fully functional!{RESET}")
    print(f"{GREEN}{'🎉 '*10}{RESET}\n")
else:
    print(f"\n{YELLOW}⚠ Some tests failed. Check the output above for details.{RESET}\n")

print(f"{BLUE}{'='*70}{RESET}")
print(f"{BLUE}   Test Data Summary{RESET}")
print(f"{BLUE}{'='*70}{RESET}\n")
print(f"User 1 ID: {test_data['user1_id']}")
print(f"User 2 ID: {test_data['user2_id']}")
print(f"Gym ID: {test_data['gym_id']}")
print(f"Session ID: {test_data['session_id']}")
print(f"Request ID: {test_data['request_id']}")
print()
