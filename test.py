import requests

with open('example.xml') as example_file:
    example = example_file.read()

print(len(example))

url = 'http://localhost:8000/stock/api/mutate/'

with open('example.xml', 'rb') as f:
    response = requests.post(
        url,
        data=f,
        headers={'Content-Type': 'application/xml'}
    )

print(response.status_code)
