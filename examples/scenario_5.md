# Scenario 5 - Create a live session

To perform this scenario, use the `create_live_session` API from `live_session.py`.

```python
import requests

base_url = "http://localhost:port/"                # To be replaced by actual port
headers = {
"Content-Type": "application/json"
}
create_session_data = {"session_name": "test_live_session"}

create_session_response = requests.post(base_url + "create_live_session/", headers=headers, json=create_session_data)

if create_session_response.status_code==201:
    print("Successfully created live session.")
else:
    print("Failed to create live session.")
```
