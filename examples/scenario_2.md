# Scenario 2 - Find a widget in the UI and perform double click on it

To perform this scenario, use the `find_element` and `double_click` APIs from `query.py` and `mouse.py`.

```python
import requests

base_url = "http://localhost:port/"               # To be replaced by actual port
headers = {
"Content-Type": "application/json"
}
data = {
"locator": "<locator_value>"              # Path of the widget to be queried
}

response = requests.post(base_url + "find_element/", headers=headers, json=data)

if response.status_code == 201:
    result = response.json()
    element_id = result["element_id"]
    message = result["message"]
    properties = result["properties"]
    print(
        f"Element found with ID {element_id}. Message: {message}. Properties: {properties}"
    )
else:
    print(
        f"Request failed with status code {response.status_code}. Error: {response.text}"
    )


click_data = {
    "element_id": element_id,  # Received in response of find_element API
    "bring_to_front": False,   # Optional field, brings the widget to focus
}
mouse_response = requests.post(base_url + "click/", headers=headers, json=click_data)

if mouse_response.status_code == 201:
    result = response.json()
    print("Element was clicked.")
else:
    print("Element was not clicked.")
```
