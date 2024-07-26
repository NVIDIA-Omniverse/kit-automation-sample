# Omniverse Code Sample - KIT Control

## Table of Contents

- [Omniverse Code Sample - KIT Control](#omniverse-code-sample---kit-control)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [How it works?](#how-it-works)
  - [API Catalog](#api-catalog)
  - [Repository Structure](#repository-structure)
  - [Quick Start](#quick-start)
    - [Prerequisite](#prerequisite)
    - [Setup](#setup)
      - [1. Clone the repository](#1-clone-the-repository)
      - [2. Importing into Omniverse KIT application](#2-importing-into-omniverse-kit-application)
      - [3. Swagger Documentation](#3-swagger-documentation)
    - [Basic Usage](#basic-usage)
      - [Scenario 1 - _Find single and multiple widgets in the UI_](#scenario-1---find-single-and-multiple-widgets-in-the-ui)
        - [Single widget](#single-widget)
        - [Multiple Widgets](#multiple-widgets)
      - [Scenario 2 - _Find a widget in the UI and perform double click on it_](#scenario-2---find-a-widget-in-the-ui-and-perform-double-click-on-it)
      - [Scenario 3 - _Find a widget in the UI and send keys on it_](#scenario-3---find-a-widget-in-the-ui-and-send-keys-on-it)
      - [Scenario 4 - _Right click and select context menu options_](#scenario-4---right-click-and-select-context-menu-options)
      - [Scenario 5 - _Create a live session_](#scenario-5---create-a-live-session)
      - [Scenario 6 - _Camera Fly forward in the scene for 5 seconds and then backwards for 5 seconds_](#scenario-6---camera-fly-forward-in-the-scene-for-5-seconds-and-then-backwards-for-5-seconds)
  - [License](#license)
  - [Contributing](#contributing)

## Overview

Welcome to the `KIT Control` repository, which demonstrates how we can automate Omniverse KIT applications using the services framework, part of the KIT SDK. This repository provides a code sample for a REST API interface that enables users to control Omniverse KIT applications by sending various interaction commands. This code sample includes various REST APIs for different UI and non-UI interactions with the application.

## How it works?

`KIT Control` allows us to control KIT from an external entity. This extension enables remote UI interactions on the app running on a separate machine from the test itself or even on the same machine. It achieves this by wrapping mouse and keyboard simulation commands from the `ui_test` extension into REST APIs, which can then be accessed over the network using the existing server backend provided by KIT.

The remote interaction feature allows us to perform complex scenarios, such as controlling multiple KIT instances on different machines synchronously and conducting remote UI interactions. This capability extends to localhost interactions as well.

Backend utilizes the core of the Omniverse microservices stack, `omni.services.core`, which holds all base components to get started with microservices in Omniverse. `omni.services.core` uses the Kit runtime to execute the code, taking advantage of an extremely powerful extension system that provides the necessary abstractions to compose and build small and efficient apps.

`omni.services.core` uses two libraries at its core to ensure that the services follow standards as defined by OpenAPI:

1. FastAPI: This library provides omni.services.core with a Router object that endpoints are registered with, helping with the auto-generation of the OpenAPI specification and allowing the dependency injection of Facilities.
2. Pydantic: Pydantic helps create well-documented and clearly-defined service payloads.

Any other extension within Omniverse can, via microservices, be exposed and triggered from external applications, and machines. They can be running alongside the main application, within the same process, or an external process.

More information about `Services` framework in Omniverse KIT can be found [here](https://docs.omniverse.nvidia.com/services/latest/index.html).

## API Catalog

This repository features sample REST APIs for various UI and Non-UI interactions with the application, categorized as follows:

| API Tag      | Purpose                                                   |
| ------------ | --------------------------------------------------------- |
| query        | Querying widgets and windows using it's unique path       |
| mouse        | Mouse events like click, right click, double click, etc   |
| keyboard     | Keyboard events like send_keys, key combo, etc            |
| menu         | Menu options selections and querying                      |
| viewport     | Viewport interactions zoom, pan, rotate, etc              |
| widget       | Widget manipulations for comboboxes & multifloatdragfield |
| window       | Window interactions close, resize, dock, etc              |
| live_session | Live Session creation, joining and exit                   |
| nucleus      | Nucleus operations file list, delete, create folder       |
| extension    | List installed extensions                                 |
| usd          | Prim USD properties transform, visibility, materials      |
| coverage     | Calculate code coverage report                            |
| misc         | Miscellaneous APIs status, wait, stage load               |

## Repository Structure

| Directory Item | Purpose                                        |
| -------------- | ---------------------------------------------- |
| .vscode        | VS Code configuration details and helper tasks |
| extensions/    | Code Sample for `kit_control` extension        |
| .gitignore     | Git configuration.                             |
| LICENSE.txt    | License for the repo.                          |
| README.md      | Project information.                           |
| SECUTIRY.md    | Security documentation for the repo.           |

## Quick Start

This section guides you through importing this code sample as an extension into your Omniverse KIT application and its basic usage

### Prerequisite

This sample assumes that an Omniverse KIT application is already installed and set up in your system.

### Setup

#### 1. Clone the repository

Begin by cloning the `main` branch from this repo to your local workspace.

If you are using windows, it is recommended to clone to a short directory path like C:/repos to avoid any file-path length issues (unless your workspace is configured to remove these limits).

#### 2. Importing into Omniverse KIT application

1. Navigate to the location where your KIT application is present, locate the `bat` or `sh` file used to start the application.
2. Via command line, we can add a single extension path to be loaded during startup along with enabling it.
3. Refer following command as example: `app.bat --ext-folder path_to_the_extensions_folder --enable kit_control`.
   1. Replace `app.bat` with the actual file name and `ext-folder` with the actual path of the `extensions` folder.

#### 3. Swagger Documentation

1. The application may or may not have a default port defined, which is used to host endpoints.
2. If the port is defined, use `http://localhost:port` to access the swagger documentation. If no port is defined, the default port set in the code sample is `9682`.

### Basic Usage

This section covers a few basic scenarios to help understand how the APIs are structured:

#### Scenario 1 - _Find single and multiple widgets in the UI_

To perform this scenario, use the `find_element` and `find_elements` APIs from `query.py`.

##### Single widget

```python
import requests

url = "http://localhost:port/find_element/"        # To be replaced by actual port
headers = {
"Content-Type": "application/json"
}
data = {
"locator": "<locator_value>"               # Path of the widget to be queried
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 201:
  result = response.json()
  element_id = result["element_id"]
  message = result["message"]
  properties = result["properties"]
  print(f"Element found with ID {element_id}. Message: {message}. Properties: {properties}")
else:
  print(f"Request failed with status code {response.status_code}. Error: {response.text}")
```

##### Multiple Widgets

```python
import requests

url = "http://localhost:port/find_elements/"       # To be replaced by actual port
headers = {
"Content-Type": "application/json"
}
data = {
"locator": "<locator_value>",               # Path of the widget to be queried
"get_properties": True
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 201:
    result = response.json()
    elements = result["elements"]
    count = result["count"]
    print(f"Found {count} elements. Details:")
    for element in elements:
        element_id = element["element_id"]
        message = element["message"]
        properties = element["properties"]
        print(f"Element ID: {element_id}. Message: {message}. Properties: {properties}")
else:
    print(f"Request failed with status code {response.status_code}. Error: {response.text}")
```

#### Scenario 2 - _Find a widget in the UI and perform double click on it_

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

#### Scenario 3 - _Find a widget in the UI and send keys on it_

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

#### Scenario 4 - _Right click and select context menu options_

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

#### Scenario 5 - _Create a live session_

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

#### Scenario 6 - _Camera Fly forward in the scene for 5 seconds and then backwards for 5 seconds_

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
    x = center["x"]
    y = center["y"]
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

## License

This repository contains software governed by the [LICENSE](LICENSE.txt) and NVIDIA Omniverse software and materials. NVIDIA Omniverse is governed by the [NVIDIA Agreements | Enterprise Software | NVIDIA Software License Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-software-license-agreement/) and [NVIDIA Agreements | Cloud Services | Service-Specific Terms for NVIDIA Omniverse Cloud](https://www.nvidia.com/en-us/agreements/cloud-services/service-specific-terms-for-omniverse-cloud/). By downloading or using NVIDIA Omniverse, you agree to the NVIDIA Omniverse terms

## Contributing

We provide this source code as-is and are currently not accepting outside contributions.
