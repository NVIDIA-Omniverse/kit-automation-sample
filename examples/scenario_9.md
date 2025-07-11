# Scenario 9 - Interact with the Live State Widget dropdown using its center position

To perform this scenario, use the `/live_menu_center` API to get the center of the "Live State Widget" button, then use the `/click_at/` API to click at an offset to interact with the dropdown on the right side of the button.

```python
import requests
import time

base_url = "http://localhost:port/"  # Replace with actual port
headers = {
    "Content-Type": "application/json"
}

# 1. Get the center of the Live State Widget button
center_response = requests.get(base_url + "live_menu_center")
if center_response.status_code == 200:
    center_data = center_response.json()["Live Menu Center"]
    x = center_data["x"]
    y = center_data["y"]
    print(f"Live State Widget center: x={x}, y={y}")
else:
    print(f"Failed to get Live Menu Center. Error: {center_response.text}")
    exit()

# 2. Click at an offset to interact with the dropdown on the right side
x_offset = 50  # Adjust this offset as needed to reach the dropdown
click_data = {
    "x": x + x_offset,
    "y": y,
    "right": False,
    "double": False
}

# Optionally, move the mouse first (not required, but can help with UI feedback)
mouse_move_data = {
    "x": x + x_offset,
    "y": y
}
move_response = requests.post(base_url + "mouse_move/", headers=headers, json=mouse_move_data)
time.sleep(1)  # Wait for UI to update

# Now perform the click
click_response = requests.post(base_url + "click_at/", headers=headers, json=click_data)
if click_response.status_code == 201:
    print("Successfully clicked at the dropdown next to Live State Widget.")
else:
    print(f"Failed to click at the dropdown. Error: {click_response.text}")
```

This approach allows you to programmatically interact with UI elements that are positioned relative to the Live State Widget, such as dropdowns or buttons to its right.
