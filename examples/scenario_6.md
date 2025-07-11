# Scenario 6 - Camera Fly forward in the scene for 5 seconds and then backwards for 5 seconds

To perform this scenario, use the `send_key_events`, and `right_click` APIs from `keyboard.py` and `mouse.py`.

```python
import requests

# Define the API endpoint
url = "http://localhost:port"

# 1. Find a widget using its path
find_element_url = f"{url}/find_element/"
find_element_data = {
    "locator": "Viewport//Frame/**/VStack[0]",
}
find_element_response = requests.post(find_element_url, json=find_element_data)

if find_element_response.status_code == 201:
    element_id = find_element_response.json()["element_id"]
    print(f"Element found with ID: {element_id}")
    center = find_element_response.json()["properties"]["center"]
    x = center[0]
    y = center[1]
else:
    print("Failed to find element")
    exit()

# 2. Perform a right-click-and-hold operation
send_mouse_events_url = f"{url}/send_mouse_events/"
click_and_hold_data = {
    "x": x,
    "y": y,
    "right": True,
    "hold": True,
    "release": False,
}
click_and_hold_response = requests.post(send_mouse_events_url, json=click_and_hold_data)

if click_and_hold_response.status_code == 201:
    print("Right-click-and-hold performed")
else:
    print("Failed to perform right-click-and-hold")
    exit()

# 3. Send keyboard event for W key and hold the button for 5 seconds
key_press_url = f"{url}/send_key_events/"
key_press_data = {
    "combo": "W",
    "hold": False,
    "release": False,
    "hold_duration": 5,
}
key_press_response = requests.post(key_press_url, json=key_press_data)

if key_press_response.status_code == 201:
    print("W key pressed and held for 5 seconds")
else:
    print("Failed to press and hold W key")
    exit()

# 4. Send keyboard event for S key and hold the button for 5 seconds
key_press_data = {
    "combo": "S",
    "hold": False,
    "release": False,
    "hold_duration": 5,
}
key_press_response = requests.post(key_press_url, json=key_press_data)

if key_press_response.status_code == 201:
    print("S key pressed and held for 5 seconds")
else:
    print("Failed to press and hold S key")
    exit()

# 5. Release the right click
release_data = {
    "x": x,
    "y": y,
    "right": True,
    "hold": False,
    "release": True,
}
release_response = requests.post(send_mouse_events_url, json=release_data)

if release_response.status_code == 201:
    print("Right click released")
else:
    print("Failed to release right click")
    exit()
```
