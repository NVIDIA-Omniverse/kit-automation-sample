# Omniverse KIT Automation Code Sample - omni.kit.test.automation.sample

## Table of Contents

- [Omniverse KIT Automation Code Sample - omni.kit.test.automation.sample](#omniverse-code-sample---omni.kit.test.automation.sample)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [How it works?](#how-it-works)
  - [API Catalog](#api-catalog)
  - [Repository Structure](#repository-structure)
  - [Quick Start](#quick-start)
    - [Prerequisite](#prerequisite)
    - [Setup](#setup)
      - [1. Clone the repository](#1-clone-the-repository)
      - [2. Creating USD Composer from Template](#2-creating-usd-composer-from-template)
      - [3. Importing into Omniverse KIT application](#3-importing-into-omniverse-kit-application)
      - [4. Swagger Documentation](#4-swagger-documentation)
    - [Basic Usage](#basic-usage)
      - [Scenario 1 - _Find single and multiple widgets in the UI_](examples/scenario_1.md)
      - [Scenario 2 - _Find a widget in the UI and perform double click on it_](examples/scenario_2.md)
      - [Scenario 3 - _Find a widget in the UI and send keys on it_](examples/scenario_3.md)
      - [Scenario 4 - _Right click and select context menu options_](examples/scenario_4.md)
      - [Scenario 5 - _Create a live session_](examples/scenario_5.md)
      - [Scenario 6 - _Camera Fly forward in the scene for 5 seconds and then backwards for 5 seconds_](examples/scenario_6.md)
      - [Scenario 7 - _Interact with menu items (e.g., Create/Mesh/Cone, File/Save)_](examples/scenario_7.md)
      - [Scenario 8 - _Switch application mode (e.g., review, layout)_](examples/scenario_8.md)
      - [Scenario 9 - _Interact with the Live State Widget dropdown using its center position_](examples/scenario_9.md)
      - [Scenario 10 - _Interact with Viewport Toolbar Buttons (e.g., Dolly, Pan)_](examples/scenario_10.md)
      - [Scenario 11 - _Interact with Viewport Menu Options (e.g., Toggle Inertia Mode)_](examples/scenario_11.md)
  - [License](#license)
  - [Contributing](#contributing)

## Overview

This Omniverse Kit Extension sample demonstrates how developers can automate testing of Omniverse Kit applications using the Kit SDK services framework. The sample makes use of a REST API interface enabling users and processes to control Omniverse Kit applications by sending various commands to execute UI and non-UI interactions. Developers are encouraged to use the sample as a starting point for implementing automated testing specific to their own Kit applications.

## How it works?

`omni.kit.test.automation.sample` allows us to control KIT from an external entity. This extension enables remote UI interactions on the app running on a separate machine from the test itself or even on the same machine. It achieves this by wrapping mouse and keyboard simulation commands from the `ui_test` extension into REST APIs, which can then be accessed over the network using the existing server backend provided by KIT.

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
| extensions/    | Code Sample for `omni.kit.test.automation.sample` extension        |
| .gitignore     | Git configuration.                             |
| LICENSE.txt    | License for the repo.                          |
| README.md      | Project information.                           |
| SECUTIRY.md    | Security documentation for the repo.           |

## Quick Start

This section guides you through importing this code sample as an extension into your Omniverse KIT application and its basic usage

### Prerequisite

This sample requires an Omniverse KIT application to run. You can either:
- Use an existing Omniverse KIT application that's already installed on your system, or
- Create a new USD Composer application using the Kit Application Template (covered in Step 2 below)

### Setup

#### 1. Clone the repository

Begin by cloning the `main` branch from this repo to your local workspace.

If you are using windows, it is recommended to clone to a short directory path like C:/repos to avoid any file-path length issues (unless your workspace is configured to remove these limits).

#### 2. Creating USD Composer from Template

If you want to work with USD Composer specifically, you can create it directly from the Kit Application Template (KAT):

1. Clone the [Kit Application Template](https://github.com/NVIDIA-Omniverse/kit-app-template) repository
2. Run the template creation tool:
   - **Linux:** `./repo.sh template new`
   - **Windows:** `.\repo.bat template new`
3. Select "Application" when prompted
4. Choose "USD Composer" from the available templates
5. Follow the configuration wizard to set up your USD Composer application

This method provides a complete USD Composer application setup optimized for authoring complex OpenUSD scenes and configurators.

#### 3. Importing the Automation Extension

Import the automation extension into your KIT application (either an existing one or the USD Composer created in Step 2):

1. Navigate to the location where your KIT application is present, locate the `bat` or `sh` file used to start the application.
2. Via command line, add the extension path and enable it during startup.
3. Use the following command as example: `app.bat --ext-folder path_to_the_extensions_folder --enable omni.kit.test.automation.sample`.
   1. Replace `app.bat` with the actual file name and `ext-folder` with the actual path of the `extensions` folder from Step 1.

#### 4. Swagger Documentation

1. The application may or may not have a default port defined, which is used to host endpoints.
2. If the port is defined, use `http://localhost:port/docs` to access the swagger documentation. If no port is defined, the default port set in the code sample is `9682`.

### Basic Usage

All scenario examples have been moved to their own files for clarity and better organization. Please see the following files for detailed usage examples:

- [Scenario 1 - Find single and multiple widgets in the UI](examples/scenario_1.md)
- [Scenario 2 - Find a widget in the UI and perform double click on it](examples/scenario_2.md)
- [Scenario 3 - Find a widget in the UI and send keys on it](examples/scenario_3.md)
- [Scenario 4 - Right click and select context menu options](examples/scenario_4.md)
- [Scenario 5 - Create a live session](examples/scenario_5.md)
- [Scenario 6 - Camera Fly forward in the scene for 5 seconds and then backwards for 5 seconds](examples/scenario_6.md)
- [Scenario 7 - Interact with menu items (e.g., Create/Mesh/Cone, File/Save)](examples/scenario_7.md)
- [Scenario 8 - Switch application mode (e.g., review, layout)](examples/scenario_8.md)
- [Scenario 9 - Interact with the Live State Widget dropdown using its center position](examples/scenario_9.md)
- [Scenario 10 - Interact with Viewport Toolbar Buttons (e.g., Dolly, Pan)](examples/scenario_10.md)
- [Scenario 11 - Interact with Viewport Menu Options (e.g., Toggle Inertia Mode)](examples/scenario_11.md)

## License

This repository contains software governed by the [LICENSE](LICENSE.txt) and NVIDIA Omniverse software and materials. NVIDIA Omniverse is governed by the [NVIDIA Agreements | Enterprise Software | NVIDIA Software License Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-software-license-agreement/) and [NVIDIA Agreements | Cloud Services | Service-Specific Terms for NVIDIA Omniverse Cloud](https://www.nvidia.com/en-us/agreements/cloud-services/service-specific-terms-for-omniverse-cloud/). By downloading or using NVIDIA Omniverse, you agree to the NVIDIA Omniverse terms

## Contributing

We provide this source code as-is and are currently not accepting outside contributions.
