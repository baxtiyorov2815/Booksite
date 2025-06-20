import requests
from getpass import getpass

auth_endpoint = "http://localhost:8000/api/auth/"
email = input("Enter your email: ")
password = getpass()
auth_response = requests.post(auth_endpoint, data={'email': email, 'password': password})
# print("Authentication Response:", auth_response.status_code)
# print("Response Content:", auth_response.content.decode('utf-8'))
print(auth_response.json())

if auth_response.status_code == 200:
    token = auth_response.json()['token']
    headers = {
        "Authorization": f"Token {token}"
    }
    endpoint = "http://localhost:8000/api/books/"
    get_response = requests.get(endpoint, headers=headers)
    print(get_response.json())