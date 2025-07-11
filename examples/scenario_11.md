# Scenario 11 - Interact with Viewport Menu Options (e.g., Toggle Inertia Mode)

Some KIT-based applications provide menu options in the viewport, often located at the top right. You can interact with these options programmatically using the `find_element`, `click`, and `click_at` APIs. This example demonstrates how to toggle the "Inertia" mode in the viewport navigation settings.

> **Note:** The widget paths for these menu options may vary between applications and versions. You will need to inspect your own app's UI to determine the correct path. The example below uses paths that work in some USD Explorer builds, but may not work everywhere.

```python
import requests
import time

base_url = "http://localhost:port/"  # Replace with actual port
headers = {
    "Content-Type": "application/json"
}

# Path to the settings hamburger (three lines) menu in the viewport
settings_menu_path = "Viewport//Frame/**/Menu[0]/Menu[0]"  # Hamburger menu
navigation_settings_path = "Viewport//Frame/**/Menu[0]/Menu[0]/Menu[0]"
inertia_mode_path = "Viewport//Frame/**/Menu[0]/Menu[0]/Menu[0]/MenuItem[6]"

# 1. Open the viewport settings menu
find_settings = {"locator": settings_menu_path}
settings_response = requests.post(base_url + "find_element/", headers=headers, json=find_settings)
if settings_response.status_code == 201:
    settings_id = settings_response.json()["element_id"]
    requests.post(base_url + "click/", headers=headers, json={"element_id": settings_id, "bring_to_front": False})
    print("Opened viewport settings menu.")
else:
    print(f"Failed to find viewport settings menu. Error: {settings_response.text}")
    exit()

# 2. Open the navigation settings submenu
find_nav = {"locator": navigation_settings_path}
nav_response = requests.post(base_url + "find_element/", headers=headers, json=find_nav)
if nav_response.status_code == 201:
    nav_id = nav_response.json()["element_id"]
    requests.post(base_url + "click/", headers=headers, json={"element_id": nav_id, "bring_to_front": False})
    print("Opened navigation settings submenu.")
else:
    print(f"Failed to find navigation settings submenu. Error: {nav_response.text}")
    exit()

# 3. Find the inertia mode menu item and get its center
find_inertia = {"locator": inertia_mode_path}
inertia_response = requests.post(base_url + "find_element/", headers=headers, json=find_inertia)
if inertia_response.status_code == 201:
    inertia_id = inertia_response.json()["element_id"]
    inertia_center = inertia_response.json()["properties"]["center"]
    print(f"Found inertia menu item at center: {inertia_center}")
else:
    print(f"Failed to find inertia menu item. Error: {inertia_response.text}")
    exit()

# 4. Toggle inertia ON (double click at an offset to the right of the center)
time.sleep(2)  # Wait for UI to update if needed
click_at_data = {
    "x": inertia_center[0] + 40,  # First element is x coordinate
    "y": inertia_center[1],       # Second element is y coordinate
    "double": True
}
click_at_response = requests.post(base_url + "click_at/", headers=headers, json=click_at_data)
if click_at_response.status_code == 201:
    print("Toggled inertia ON via menu.")
else:
    print(f"Failed to toggle inertia. Error: {click_at_response.text}")

# Optionally, take a screenshot or perform other actions here
```

You can use a similar approach for other menu options by updating the widget paths accordingly. Use the UI inspector to determine the correct path for your application.
