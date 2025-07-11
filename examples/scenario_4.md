# Scenario 4 - Right click and select context menu options

To perform this scenario, use the `find_element`, `click` and `context_menu_select` APIs from `query.py`, `menu.py` and `mouse.py`.

```python
import requests

base_url = "http://localhost:port"                # To be replaced by actual port
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

double_click_data = {
  "element_id":element_id,                  # Received in response of find_element API
  "bring_to_front": False                   # Optional field, brings the widget to focus
}
mouse_response = requests.post(
    base_url + "right_click/", headers=headers, json=double_click_data
)

menu_data ={
  "path": "menu_path",                      # / separated path like Create/Prims/Cone
  "offset_x": 50,                           # Optional field
  "offset_y": 0,                            # Optional field
  "human_delay_speed": 10                   # Optional field
}

menu_response = requests.post(
    base_url + "context_menu_select/", headers=headers, json=menu_data
)

if menu_response.status_code == 201:
    print("Successfully selected the context menu option.")
else:
    print("Failure in selecting context menu option.")
```
