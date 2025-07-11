# Scenario 3 - Find a widget in the UI and send keys on it

To perform this scenario, use the `find_element` and `send_keys_to_element` APIs from `query.py` and `keyboard.py`.

```python
import requests

base_url = "http://localhost:port/"                # To be replaced by actual port
headers = {
"Content-Type": "application/json"
}
data = {
"locator": "<locator_value>"               # Path of the widget to be queried
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

send_keys_data = {
  "element_id":element_id,                  # Received in response of find_element API
  "text": "hello",
  "human_delay_speed": 20                   # Optional field to set the typing speed
}
keyboard_response = requests.post(
    base_url + "send_keys_to_element/", headers=headers, json=send_keys_data
)

if keyboard_response.status_code == 201:
    result = response.json()
    print("Successfully sent keys to the element.")
else:
    print("Failure in sending keys to the element.")
```
