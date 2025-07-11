# Scenario 8 - Switch application mode (e.g., review, layout)

To perform this scenario, use the `switch_app_mode` API from `misc.py`.

```python
import requests

base_url = "http://localhost:port/"  # Replace with actual port
headers = {
    "Content-Type": "application/json"
}

# Example: Switch to 'review' mode
mode_response = requests.post(base_url + "switch_app_mode/?option_name=review", headers=headers)

if mode_response.status_code == 201:
    print("Successfully switched to 'review' mode.")
else:
    print(f"Failure in switching app mode. Error: {mode_response.text}")

# Example: Switch to 'layout' mode
mode_response = requests.post(base_url + "switch_app_mode/?option_name=layout", headers=headers)

if mode_response.status_code == 201:
    print("Successfully switched to 'layout' mode.")
else:
    print(f"Failure in switching app mode. Error: {mode_response.text}")
```
