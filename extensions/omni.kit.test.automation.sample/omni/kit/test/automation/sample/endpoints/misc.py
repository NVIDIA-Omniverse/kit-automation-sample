# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.


import asyncio
import logging
import os
import base64
from typing import Dict, List

from fastapi import HTTPException
from fastapi.responses import FileResponse
from omni.kit import ui_test
from omni.services.core import routers
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from ..api_models.common_models import MessageResponse
from ..api_models.misc_models import (
    ScreenshotRequest,
    ScreenshotResponse,
    StageLoadRequest,
)

logger = logging.getLogger("omni.kit.test.automation.sample")

router = routers.ServiceAPIRouter()

# Constants for log messages to avoid user-controlled data in format strings
LOG_MODE_SELECT_FAILED = "Failed to select mode"
LOG_MODE_SWITCHED = "Switched to mode option"
LOG_MODE_NOT_AVAILABLE = "App modes are not available in this application"
LOG_MODE_NOT_FOUND = "Option with name not found"
LOG_MODE_CHANGE_ERROR = "Unable to change Application Mode"


def _encode_for_logging(text: str) -> str:
    """Safely encode user-controlled text for logging."""
    if text.isalnum():
        return text
    return f"(encoded){base64.b64encode(text.encode('UTF-8')).decode('UTF-8')}"


@router.get("/automation_sample_status", tags=["Automation Sample Status"])
async def automation_sample_status():
    """
        Status check API for automation sample extension

    This function returns the status of the automation sample extension. It returns a dictionary containing the status "OK" if the extension is running.

    Returns:

        Dict[str, str]: A response dictionary containing the status of the extension.
    """
    return {"status": "OK"}


@router.post(
    "/wait_frames/",
    response_model=MessageResponse,
    status_code=HTTP_201_CREATED,
    tags=["Waits"],
)
async def wait_frames(frames: int):
    """
        Waits for a specified number of frames.

    Parameters:

        frames (int): The number of frames to wait.

    Returns:

        MessageResponse: A message indicating that the wait was successful.

    Raises:

        HTTPException: If there is an error while waiting.
    """
    try:
        await ui_test.human_delay(frames)
        msg = f"Waited for {frames} frames to be updated"
        logger.info(msg)
        return MessageResponse(message=msg)
    except Exception as e:
        msg = f"System did not wait for {frames} frames due to error {str(e)}"
        logger.error(msg)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)


@router.post(
    "/wait_for_stage_load/",
    response_model=MessageResponse,
    status_code=HTTP_201_CREATED,
    tags=["Waits"],
)
async def wait_for_stage_load(request: StageLoadRequest):
    """
        Waits for the stage to load or for the specified number of frames to pass.

    This endpoint waits for the stage to finish loading or for the specified number of frames to pass,
    whichever happens first. If the stage finishes loading within the specified number of frames,
    a success message is returned. If the stage does not finish loading even after waiting for the
    specified number of frames, a server error is raised.

    Parameters:

        frames (int): The number of frames to wait for before giving up.
        seconds (int): The number of seconds to wait for before giving up.

    Returns:

        A MessageResponse object containing a success or error message.

    Raises:

        HTTPException: If the stage does not finish loading even after waiting for the specified number of frames.
    """
    import time

    import omni.usd

    flag = False
    start = time.time()
    end = start + request.seconds
    usd_context: omni.usd.UsdContext = omni.usd.get_context()
    frame_count = 0
    while time.time() < end and frame_count < request.frames:
        path, files_loaded, total_files = usd_context.get_stage_loading_status()
        logger.info(
            f"Path - {path}, Files Loaded - {files_loaded}, Total Files - {total_files}"
        )
        if files_loaded or total_files:
            logger.info("Waiting for all assets to get loaded.")
            await omni.kit.app.get_app().next_update_async()
            continue
        if not files_loaded or not total_files:
            flag = True
        if not flag and frame_count != request.frames:
            logger.info(f"Waiting for {request.frames} frames.")
            await omni.kit.app.get_app().next_update_async()
            frame_count += 1
            continue

        break

    await omni.kit.app.get_app().next_update_async()
    await omni.kit.app.get_app().next_update_async()

    if flag:
        msg = f"Stage has been successfully loaded within {request.frames} frames and {request.seconds} seconds."
        logger.info(msg)
        return MessageResponse(message=msg)
    else:
        msg = f"Stage load failed even after waiting for {request.frames} frames and {request.seconds} seconds."
        logger.error(msg)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)


@router.get("/stage/", response_model=Dict[str, List], tags=["Misc"])
async def stage():
    """
        Gets the current stage from the USD context and returns a dictionary containing all prims and selected prims in the stage.

    Returns:

        Dict[str, List]: A dictionary containing:
            - 'all_prims': A list of strings representing all prims in the stage.
            - 'selected_prims': A list of strings representing the currently selected prims in the stage.

    Raises:

        HTTPException: If there is an error getting the stage from the USD context.
    """
    from omni import usd

    try:
        stage = usd.get_context().get_stage()
        prims = [str(x) for x in stage.Traverse()]
        selection = usd.get_context().get_selection().get_selected_prim_paths()
        return {"all_prims": prims, "selected_prims": selection}
    except Exception as e:
        msg = f"Unable to get stage from USD Context {str(e)}"
        logger.error(msg)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)


@router.post(
    "/switch_app_mode/",
    response_model=MessageResponse,
    status_code=HTTP_201_CREATED,
    tags=["Misc"],
)
async def switch_app_mode(option_name: str):
    """
        Switch the application mode or renderer mode based on the provided option name.

    `Note`:

        This operation will only work on applications that have different modes available.

    Parameters:

        option_name (str): The name of the mode to switch to.

    Returns:

        MessageResponse: A response object containing a success message.

    Raises:

        HTTPException: If the option name is not found or an error occurs during the process.
    """
    from omni import ui
    from omni.kit.ui_test import Vec2
    from omni.ui_query import OmniUIQuery

    try:
        menu_bar = OmniUIQuery.find_menu_item(
            "Application Mode Widget"
        )  # Finds the menu bar

        for widget in OmniUIQuery.find_widgets("*", [menu_bar]):
            if isinstance(widget, ui.Menu) or isinstance(widget, ui.MenuItem):
                if widget.text == "Application Mode Widget":
                    all_buttons = {}
                    amc = widget.delegate.application_control
                    if amc:
                        all_buttons.update(amc.button_group.children)
                    rmc = widget.delegate.render_control
                    if rmc:
                        all_buttons.update(rmc.button_group.children)
                    target_button = all_buttons[option_name.lower()]
                    center = Vec2(target_button.screen_position) + Vec2(
                        target_button._label.computed_width / 2,
                        target_button._label.computed_height / 2,
                    )
                    await ui_test.emulate_mouse_move_and_click(center)
                    if not target_button.selected:
                        encoded_option = _encode_for_logging(option_name)
                        logger.error("%s: '%s'", LOG_MODE_SELECT_FAILED, encoded_option)
                        raise HTTPException(
                            status_code=HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=f"{LOG_MODE_SELECT_FAILED}: '{option_name}'"
                        )

                    encoded_option = _encode_for_logging(option_name)
                    logger.info("%s: '%s'", LOG_MODE_SWITCHED, encoded_option)
                    return MessageResponse(message=f"Switched to '{option_name}' option.")
        logger.error(LOG_MODE_NOT_AVAILABLE)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, 
            detail=LOG_MODE_NOT_AVAILABLE
        )
    except KeyError:
        encoded_option = _encode_for_logging(option_name)
        logger.error("%s: %s", LOG_MODE_NOT_FOUND, encoded_option)
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, 
            detail=f"{LOG_MODE_NOT_FOUND}: {option_name}"
        )
    except HTTPException as e:
        # If the HTTPException is raised, it means that the option name is not found.
        # So, we need to raise the same HTTPException.
        raise e
    except Exception as e:
        encoded_option = _encode_for_logging(option_name)
        logger.error("%s: %s. Error: %s", LOG_MODE_CHANGE_ERROR, encoded_option, str(e))
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"{LOG_MODE_CHANGE_ERROR}: {encoded_option}. Error: {str(e)}"
        )


@router.post(
    "/capture_full_app_screenshot/",
    response_model=ScreenshotResponse,
    status_code=HTTP_201_CREATED,
    tags=["Misc"],
)
async def capture_full_screenshot(request: ScreenshotRequest):
    """
    Capture a full application screenshot.

    This function captures a screenshot of the application and saves it to a specified directory.

    Valid formats - `png` and `jpeg`

    Path examples - `C:/users/user/screenshot.png`

    Parameters:

        request (ScreenshotRequest): The request object containing the screenshot parameters.
            - dir (str): The directory where the screenshot image will be saved.

    Returns:

        FileResponse or ScreenshotResponse: A response object containing the file path and
            message if the screenshot was saved to the server.

    Raises:

        HTTPException: An error occurred while capturing the screenshot.
    """

    import omni.renderer_capture

    if "jpeg" in request.dir or "png" in request.dir:
        try:

            renderer_capture = omni.renderer_capture.acquire_renderer_capture_interface()
            renderer_capture.capture_next_frame_swapchain(request.dir)
            msg = f"Viewport screenshot captured successfully at {request.dir}."
            logger.info(msg)
            return ScreenshotResponse(file_path=request.dir, message=msg)

        except Exception as e:
            msg = f"Error capturing screenshot: {str(e)}"
            logger.error(msg)
            raise HTTPException(status_code=500, detail=msg)
    else:
        msg = f"Error capturing viewport screenshot: Please specify the format png or jpeg"
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=msg)


@router.get("/fetch_all_materials/", response_model=Dict[str, str], tags=["Misc"])
async def fetch_all_materials():
    """
        Fetch all materials from the materials window.

    This function retrieves all materials from the materials window and returns them as a JSON
    serialized dictionary.

    `Note`:

        For all the materials to load, the material window needs to be navigated to once before
        calling this API so that all the materials get loaded.

    Returns:

        Dict[str, str]: A dictionary containing the materials data as a JSON string.

    Raises:

        HTTPException: Unable to fetch data of all materials from materials window.
    """
    import json

    from omni.kit.window.material import get_instance

    try:
        material_dict = {}

        def list_category(model, category):
            if len(category.children) == 0:
                lis = []
                for detail in model.get_item_children(category):
                    lis.append(detail.name)
                return lis
            dic = {}
            dic["self"] = []
            for detail in model.get_item_children(category):
                dic["self"].append(detail.name)
            for child in category.children:
                dic[child.name] = list_category(model, child)
            return dic

        w = get_instance()._window
        if w:
            model = w.browser_model
            if model:
                for collection in model.get_item_children(None):
                    for category in model.get_item_children(collection):
                        if category.name == "All":
                            continue
                        else:
                            material_dict[category.name] = list_category(
                                model, category
                            )
        json_data = json.dumps(material_dict)

        return {"materials": json_data}
    except Exception as e:
        msg = f"Unable to fetch data of all materials from materials window. {str(e)}"
        logger.error(msg)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
