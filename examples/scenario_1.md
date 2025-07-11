# Scenario 1 - Find single and multiple widgets in the UI

To perform this scenario, use the `find_element` and `find_elements` APIs from `query.py`.

## Single widget

```python
import requests

url = "http://localhost:port/find_element/"        # To be replaced by actual port
headers = {
"Content-Type": "application/json"
}
data = {
"locator": "<locator_value>"               # Path of the widget to be queried
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 201:
  result = response.json()
  element_id = result["element_id"]
  message = result["message"]
  properties = result["properties"]
  print(f"Element found with ID {element_id}. Message: {message}. Properties: {properties}")
else:
  print(f"Request failed with status code {response.status_code}. Error: {response.text}")
```

## Multiple Widgets

```python
import requests

url = "http://localhost:port/find_elements/"       # To be replaced by actual port
headers = {
"Content-Type": "application/json"
}
data = {
"locator": "<locator_value>",               # Path of the widget to be queried
"get_properties": True
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 201:
    result = response.json()
    elements = result["elements"]
    count = result["count"]
    print(f"Found {count} elements. Details:")
    for element in elements:
        element_id = element["element_id"]
        message = element["message"]
        properties = element["properties"]
        print(f"Element ID: {element_id}. Message: {message}. Properties: {properties}")
else:
    print(f"Request failed with status code {response.status_code}. Error: {response.text}")
```
