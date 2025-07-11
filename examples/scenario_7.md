# Scenario 7 - Interact with menu items (e.g., Create/Mesh/Cone, File/Save)

To perform this scenario, use the `menu_select` API from `menu.py`.

```python
import requests

base_url = "http://localhost:port/"  # Replace with actual port
headers = {
    "Content-Type": "application/json"
}

# Example 1: Select 'Create/Mesh/Cone' from the menu
menu_data = {
    "path": "Create/Mesh/Cone"  # Use the exact menu path as shown in the UI
}
menu_response = requests.post(base_url + "menu_select/", headers=headers, json=menu_data)

if menu_response.status_code == 201:
    print("Successfully selected 'Create/Mesh/Cone' from the menu.")
else:
    print(f"Failure in selecting menu item. Error: {menu_response.text}")

# Example 2: Select 'File/Save' from the menu
menu_data = {
    "path": "File/Save"
}
menu_response = requests.post(base_url + "menu_select/", headers=headers, json=menu_data)

if menu_response.status_code == 201:
    print("Successfully selected 'File/Save' from the menu.")
else:
    print(f"Failure in selecting menu item. Error: {menu_response.text}")
```
