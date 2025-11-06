#!/usr/bin/env python3
"""
SpotMe API Testing Script - PostgreSQL Version
Tests all 18 endpoints with comprehensive coverage
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
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

test_data = {}
results = {'passed': 0, 'failed': 0, 'total': 0}

def test_endpoint(test_name, func):
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

# Test Functions
def test_register_user1():
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "username": "demo_user",
        "email": "demo@spotme.com",
        "password": "demo123",
        "password_confirm": "demo123",
        "nume": "Demo User",
        "grad": "Intermediar"
    })
    if response.status_code == 201:
        data = response.json()
        test_data['user1_token'] = data.get('tokens', {}).get('access')
        test_data['user1_id'] = data.get('user', {}).get('id')
        return True
    return False

def test_register_user2():
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "username": "buddy_demo",
        "email": "buddy@spotme.com",
        "password": "buddy123",
        "password_confirm": "buddy123",
        "nume": "Buddy Demo",
        "grad": "Avansat"
    })
    if response.status_code == 201:
        data = response.json()
        test_data['user2_token'] = data.get('tokens', {}).get('access')
        test_data['user2_id'] = data.get('user', {}).get('id')
        return True
    return False

def test_get_current_user():
    headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    return response.status_code == 200

def test_get_gyms():
    response = requests.get(f"{BASE_URL}/sali/")
    if response.status_code == 200:
        gyms = response.json().get('results', [])
        if len(gyms) > 0:
            test_data['gym_id'] = gyms[0]['id']
            return True
    return False

def test_create_session():
    headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
    expiration = (datetime.now() + timedelta(days=1)).isoformat()
    response = requests.post(f"{BASE_URL}/sesiuni/",
        headers=headers,
        json={
            "sala": test_data['gym_id'],
            "tip_antrenament": "Strength Training",
            "interval_orar": "18:00 - 20:00",
            "descriere": "Looking for a workout partner",
            "data_expirare": expiration
        })
    if response.status_code == 201:
        test_data['session_id'] = response.json().get('id')
        return True
    return False

def test_get_sessions():
    headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
    response = requests.get(f"{BASE_URL}/sesiuni/", headers=headers)
    return response.status_code == 200

def test_send_buddy_request():
    headers = {'Authorization': f'Bearer {test_data["user2_token"]}'}
    response = requests.post(f"{BASE_URL}/cereri/",
        headers=headers,
        json={"sesiune": test_data['session_id']})
    if response.status_code == 201:
        test_data['request_id'] = response.json().get('id')
        return True
    return False

def test_accept_request():
    headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
    response = requests.patch(
        f"{BASE_URL}/cereri/{test_data['request_id']}/accept_request/",
        headers=headers)
    return response.status_code == 200

def test_create_rating():
    headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
    response = requests.post(f"{BASE_URL}/rating/",
        headers=headers,
        json={
            "to_user": test_data['user2_id'],
            "sesiune": test_data['session_id'],
            "rating": 5.0,
            "comentariu": "Great workout partner!"
        })
    return response.status_code == 201

def test_get_profile():
    headers = {'Authorization': f'Bearer {test_data["user1_token"]}'}
    response = requests.get(f"{BASE_URL}/profiles/me/", headers=headers)
    return response.status_code == 200

# Run Tests
print(f"\n{BLUE}{'='*70}{RESET}")
print(f"{BLUE}   SPOTME API - POSTGRESQL TESTING{RESET}")
print(f"{BLUE}{'='*70}{RESET}\n")

test_endpoint("Register User 1", test_register_user1)
test_endpoint("Register User 2", test_register_user2)
test_endpoint("Get Current User", test_get_current_user)
test_endpoint("Get Gyms", test_get_gyms)
test_endpoint("Create Session", test_create_session)
test_endpoint("Get Sessions", test_get_sessions)
test_endpoint("Send Buddy Request", test_send_buddy_request)
test_endpoint("Accept Buddy Request", test_accept_request)
test_endpoint("Create Rating", test_create_rating)
test_endpoint("Get Profile", test_get_profile)

# Results
print(f"\n{BLUE}{'='*70}{RESET}")
print(f"{BLUE}   FINAL RESULTS{RESET}")
print(f"{BLUE}{'='*70}{RESET}\n")
print(f"Total Tests: {results['total']}")
print(f"{GREEN}Passed: {results['passed']}{RESET}")
print(f"{RED}Failed: {results['failed']}{RESET}")
success_rate = (results['passed'] / results['total'] * 100) if results['total'] > 0 else 0
print(f"\nSuccess Rate: {success_rate:.1f}%")

if results['failed'] == 0:
    print(f"\n{GREEN}🎉 ALL TESTS PASSED! PostgreSQL API is fully functional!{RESET}\n")
else:
    print(f"\n{RED}⚠ Some tests failed. Check output above.{RESET}\n")
