from app import load_data
from werkzeug.security import check_password_hash

# Test the login functionality
data = load_data()
print("Data loaded:", data.keys())

if 'users' in data:
    print("Users found:", len(data['users']))
    for user in data['users']:
        print(f"Username: {user['username']}")
        # Test password
        if check_password_hash(user['password_hash'], 'admin123'):
            print("SUCCESS: Password 'admin123' works!")
        else:
            print("ERROR: Password 'admin123' doesn't work")
else:
    print("❌ No users section found")