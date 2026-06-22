import requests

with open('example.xml') as example_file:
    example = example_file.read()

url = 'http://localhost:8000/stock/api/mutate/'
response = requests.post(
    url,
    data=example,
    headers={
        'Content-Type': 'application/xml'
    }
)

print(response.status_code)
