# Scenario 10 - Interact with Viewport Toolbar Buttons (e.g., Dolly, Pan)

Some KIT-based applications (such as USD Explorer) provide toolbar buttons in the viewport for camera operations like dolly, pan, orbit, etc. You can interact with these buttons programmatically using the `find_element` and `click` APIs.

> **Note:** The widget path for these buttons may vary between applications and versions. You will need to inspect your own app's UI to determine the correct path. The example below uses a path that works in some USD Explorer builds, but may not work everywhere.

```python
import requests

base_url = "http://localhost:port/"  # Replace with actual port
headers = {
    "Content-Type": "application/json"
}

# Example: Enable the Dolly tool in the viewport toolbar
# You must find the correct widget path for your app. This is just an example:
dolly_btn_path = "Viewport//Frame/**/Button[0].name=='dolly'"

# 1. Find the dolly button
find_data = {
    "locator": dolly_btn_path
}
find_response = requests.post(base_url + "find_element/", headers=headers, json=find_data)

if find_response.status_code == 201:
    element_id = find_response.json()["element_id"]
    print(f"Found dolly button with element_id: {element_id}")
else:
    print(f"Failed to find dolly button. Error: {find_response.text}")
    exit()

# 2. Click the dolly button
click_data = {
    "element_id": element_id
}
click_response = requests.post(base_url + "click/", headers=headers, json=click_data)

if click_response.status_code == 201:
    print("Dolly tool enabled via toolbar button.")
else:
    print(f"Failed to click dolly button. Error: {click_response.text}")
```

You can use a similar approach for other toolbar buttons (e.g., pan, orbit) by updating the widget path accordingly. Use the UI inspector to determine the correct path for your application.
