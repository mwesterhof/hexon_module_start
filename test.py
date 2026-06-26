import requests
from requests.auth import HTTPBasicAuth

with open('example.xml') as example_file:
    example = example_file.read()

auth = HTTPBasicAuth('vzw', 'secret')
print(len(example))

url = 'http://localhost:8000/hexon/api/mutate/'

with open('example.xml', 'rb') as f:
    response = requests.post(
        url,
        data=f,
        headers={'Content-Type': 'application/xml'},
        auth=auth
    )

print(response.status_code)
