#!/usr/bin/env python3
"""
Test script to measure legal banking API performance with file uploads.
"""

import requests
import time
import os
from PIL import Image
import io

# Configuration
BASE_URL = "http://localhost:8000/api"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "testpass123"

def create_test_image(size_mb=1):
    """Create a test image of specified size in MB."""
    # Create a simple image
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color='red')
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG', quality=95)
    
    # If we need a larger file, we can repeat the image
    current_size = len(img_bytes.getvalue())
    target_size = size_mb * 1024 * 1024
    
    if current_size < target_size:
        # Create multiple copies to reach target size
        final_bytes = io.BytesIO()
        while len(final_bytes.getvalue()) < target_size:
            final_bytes.write(img_bytes.getvalue())
        return final_bytes.getvalue()
    
    return img_bytes.getvalue()

def login_user():
    """Login and get authentication token."""
    login_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    if response.status_code == 200:
        return response.json().get('token')
    else:
        print(f"Login failed: {response.status_code}")
        print(response.text)
        return None

def test_legal_banking_performance():
    """Test legal banking API performance with file uploads."""
    
    # Login
    print("Logging in...")
    token = login_user()
    if not token:
        print("Failed to login. Please ensure the server is running and test user exists.")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "multipart/form-data"
    }
    
    # Test data
    legal_data = {
        "companyType": "Private Limited Company",
        "emergencyContact": "+919876543210",
        "termsAccepted": True,
        "panOrAadhaarText": "ABCDE1234F"
    }
    
    # Test 1: Without file upload
    print("\n1. Testing without file upload...")
    start_time = time.time()
    
    response = requests.patch(
        f"{BASE_URL}/partner/legal-banking/",
        json=legal_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    duration = time.time() - start_time
    print(f"   Status: {response.status_code}")
    print(f"   Duration: {duration:.2f} seconds")
    
    # Test 2: With 1MB image
    print("\n2. Testing with 1MB image...")
    start_time = time.time()
    
    # Create test image
    image_data = create_test_image(1)
    
    files = {
        'businessProofFile': ('test_image.jpg', image_data, 'image/jpeg')
    }
    
    response = requests.patch(
        f"{BASE_URL}/partner/legal-banking/",
        data=legal_data,
        files=files,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    duration = time.time() - start_time
    print(f"   Status: {response.status_code}")
    print(f"   Duration: {duration:.2f} seconds")
    print(f"   File size: {len(image_data) / (1024*1024):.1f} MB")
    
    # Test 3: With 2MB image
    print("\n3. Testing with 2MB image...")
    start_time = time.time()
    
    # Create larger test image
    image_data_2mb = create_test_image(2)
    
    files = {
        'businessProofFile': ('test_image_2mb.jpg', image_data_2mb, 'image/jpeg')
    }
    
    response = requests.patch(
        f"{BASE_URL}/partner/legal-banking/",
        data=legal_data,
        files=files,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    duration = time.time() - start_time
    print(f"   Status: {response.status_code}")
    print(f"   Duration: {duration:.2f} seconds")
    print(f"   File size: {len(image_data_2mb) / (1024*1024):.1f} MB")
    
    # Test 4: Multiple files
    print("\n4. Testing with multiple files...")
    start_time = time.time()
    
    # Create two files
    pan_image = create_test_image(0.5)
    business_image = create_test_image(1.5)
    
    files = {
        'panOrAadhaarFile': ('pan_card.jpg', pan_image, 'image/jpeg'),
        'businessProofFile': ('business_license.jpg', business_image, 'image/jpeg')
    }
    
    response = requests.patch(
        f"{BASE_URL}/partner/legal-banking/",
        data=legal_data,
        files=files,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    duration = time.time() - start_time
    print(f"   Status: {response.status_code}")
    print(f"   Duration: {duration:.2f} seconds")
    print(f"   Total file size: {(len(pan_image) + len(business_image)) / (1024*1024):.1f} MB")
    
    print("\nPerformance test completed!")

if __name__ == "__main__":
    test_legal_banking_performance() 