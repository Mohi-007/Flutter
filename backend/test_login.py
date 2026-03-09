import requests

url = "http://127.0.0.1:5000/api/auth/register"
res = requests.post(url, json={
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "password123"
})
print("Register:", res.status_code, res.text)

url = "http://127.0.0.1:5000/api/auth/login"
res = requests.post(url, json={
    "email": "testuser@example.com",
    "password": "password123"
})
print("Login:", res.status_code, res.text)
