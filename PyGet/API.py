import requests

url = "https://api.example.com/data"
headers = {
    "Authorization": "Bearer your_api_key"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Failed to retrieve data:", response.status_code)
