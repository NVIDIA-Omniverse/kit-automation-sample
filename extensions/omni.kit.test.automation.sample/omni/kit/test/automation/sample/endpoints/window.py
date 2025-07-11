# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.


import logging
from typing import Dict, Union
import base64

import omni.ui as ui
from fastapi import HTTPException, status
from omni.services.core import routers

from ..api_models.common_models import MessageResponse
from ..api_models.window_models import (
    DockWindowRequest,
    ResizeWindowRequest,
    WindowListResponse,
)
from ..utils.element_cache import element_cache
from ..utils.omnielement import OmniElement

logger = logging.getLogger("omni.kit.test.automation.sample")

router = routers.ServiceAPIRouter()

# Constants for log messages to avoid user-controlled data in format strings
LOG_WINDOW_POSITION = "Set window position for window"
LOG_ELEMENT_NOT_WINDOW = "Element is not of type Window, actual type is"
LOG_ELEMENT_NOT_FOUND = "Element with ID not found in element cache"
LOG_MULTIPLE_WINDOWS = "Found multiple windows with name. Using first visible window found"
LOG_WINDOW_CLOSED = "Window closed"
LOG_WINDOW_NOT_FOUND = "Failed to find visible window"
LOG_WINDOW_CLOSE_ERROR = "Error occurred while closing window"
LOG_WINDOW_DIMENSIONS = "Unable to get dimensions for window"


def _encode_for_logging(text: str) -> str:
    """Safely encode user-controlled text for logging."""
    if text.isalnum():
        return text
    return f"(encoded){base64.b64encode(text.encode('UTF-8')).decode('UTF-8')}"


@router.get("/windows/", response_model=WindowListResponse, tags=["Window"])
async def windows():
    """
        Get the list of available windows in the UI.

    This endpoint retrieves the list of available windows in the UI and returns a `WindowListResponse` object containing lists of visible and all window titles.

    Returns:
    
        WindowListResponse: A pydantic model containing the following information about the windows:
            - visible_windows (List[str]): A list of paths to the visible application windows.
            - all_windows (List[str]): A list of paths to all application windows.

    Raises:
    
        HTTPException: If unable to retrieve list of windows.
    """
    visible_window_list = []
    all_windows_list = []

    try:
        windows = ui.Workspace.get_windows()
        for window in windows:
            if window.visible == True:
                visible_window_list.append(window.title)
            all_windows_list.append(window.title)
        logger.info("Windows retrieved successfully.")
        return WindowListResponse(
            visible_windows=visible_window_list, all_windows=all_windows_list
        )
    except Exception as e:
        logger.error(f"Error while retrieving windows: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.post(
    "/set_window_position/",
    status_code=status.HTTP_201_CREATED,
    response_model=MessageResponse,
    tags=["Window"],
)
async def window_position(identifier: str, x: float, y: float):
    """
        Set the window position for the given identifier.

    This endpoint sets the window position for the given identifier based on the provided x and y coordinates.
    If the element is not a window or if the element is not found in the cache, a 404 HTTP exception is raised.

    Parameters:
    
        identifier (str): The identifier of the window element received in query API response.
        x (float): The new x-coordinate of the window position.
        y (float): The new y-coordinate of the window position.

    Returns:
    
        MessageResponse: A response object containing a message about the operation.

    Raises:
    
        HTTPException: If the element is not a window or if the element is not found in the cache.
    """
    try:
        element: OmniElement = element_cache.get_cached_element(identifier)
        if (
            ui._ui.Window in element.widget.__class__.__bases__
            or ui.Window in element.widget.__class__.__bases__
            or isinstance(element.widget, (ui._ui.Window, ui.Window))
        ):
            element.widget.position_x = x
            element.widget.position_y = y
            logger.info("%s at %s: (%s,%s)", LOG_WINDOW_POSITION, element.realpath, x, y)
            return MessageResponse(message=f"Set window position as ({x},{y}) for window at {element.realpath}")
            logger.info("%s at %s: (%s,%s)", LOG_WINDOW_POSITION, element.realpath, x, y)
            return MessageResponse(message=f"Set window position as ({x},{y}) for window at {element.realpath}")
        else:
            logger.error("%s: %s", LOG_ELEMENT_NOT_WINDOW, element.get_type)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"{LOG_ELEMENT_NOT_WINDOW}: {element.get_type}"
            )
            logger.error("%s: %s", LOG_ELEMENT_NOT_WINDOW, element.get_type)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"{LOG_ELEMENT_NOT_WINDOW}: {element.get_type}"
            )
    except KeyError:
        encoded_id = _encode_for_logging(identifier)
        logger.error("%s: %s", LOG_ELEMENT_NOT_FOUND, encoded_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{LOG_ELEMENT_NOT_FOUND}: {identifier}"
        )


@router.post(
    "/close_window/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Window"],
)
async def close_window(window_name: str):
    """
        Close a window with the given name.

    This endpoint closes a window with the given name. If the window is not found or an error occurs while closing the window, a 404 HTTP exception is raised.

    Parameters:
    
        window_name (str): The name of the window to be closed.

    Returns:
    
        MessageResponse: A response object containing a message indicating the window has been closed.

    Raises:
    
        HTTPException: If the window is not found or an error occurs while closing the window.
    """
    windows = ui.Workspace.get_windows()
    window_list = []
    for window in windows:
        if window.title == window_name:
            window_list.append(window)
    try:
        if len(window_list) == 1:
            window = window_list[0]
        else:
            logger.warn(
                "%s: %s (%d found)", LOG_MULTIPLE_WINDOWS, _encode_for_logging(window_name), len(window_list)
            )
            window = None
            for win in window_list:
                if win.visible:
                    window = win
                    break
        if window:
            window.visible = False
            logger.info("%s: %s", LOG_WINDOW_CLOSED, _encode_for_logging(window_name))
            return MessageResponse(message=f"{window_name} window closed.")
        else:
            logger.error("%s: %s", LOG_WINDOW_NOT_FOUND, _encode_for_logging(window_name))
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"{LOG_WINDOW_NOT_FOUND}: {window_name}"
            )
    except Exception:
        logger.error("%s: %s", LOG_WINDOW_CLOSE_ERROR, _encode_for_logging(window_name))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{LOG_WINDOW_CLOSE_ERROR}: {window_name}"
        )


@router.post(
    "/resize_window/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Window"],
)
def resize_window(request: ResizeWindowRequest):
    """
        Resizes the specified window to the given height and width.
    The ID received in response of query API is used to find the window and resize it.

    Parameters:
    
        request (ResizeWindowRequest): The request body containing the following parameters:
            - id (str): The ID of the window to resize.
            - new_width (float): The new width of the window.
            - new_height (float): The new height of the window.

    Returns:
    
        MessageResponse: A response object containing a message indicating whether the window was successfully resized.

    Raises:
    
        HTTPException: If the element with the provided identifier is not found, or if the resieze action fails.
    """
    try:
        element: OmniElement = element_cache.get_cached_element(request.id)
        element.change_height(request.new_height)
        element.change_width(request.new_width)
        if element.width == request.new_width and element.height == request.new_height:
            msg = f"Resize window {element.realpath} to height {element.height} and width {element.width}"
            logger.info(msg)
            return MessageResponse(message=msg)
        else:
            msg = f"Resize window operation failed. Height Expected: {request.new_height} Actual:{element.height} Width Expected: {request.new_width} Actual:{element.width}"
            logger.error(msg)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg
            )
    except KeyError:
        msg = f"Element with ID {request.id} not found in element cache."
        logger.error(msg)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)


@router.post(
    "/dock_window/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Window"],
)
async def dock_window(request: DockWindowRequest):
    """
        Dock a window into another window.

    This endpoint allows you to dock a window into another window in the Omni Kit viewport.

    Parameters:
    
        request (DockWindowRequest): A request object containing the following fields:
            - first_window (str): The name of the window to be docked.
            - second_window (str): The name of the window to dock into.
            - dock_position (str): The position where the window should be docked. Can be one of the following: 'Left', 'Right', 'Top', 'Bottom', 'Fill'.

    Returns:
    
        MessageResponse: A response object containing a message indicating that the docking operation was successful.

    Raises:
    
        HTTPException(400): If either of the windows with the given IDs is not found or if dock position is invalid.
    """
    win_to_be_docked = ui.Workspace.get_window(request.first_window)
    win_to_dock_into = ui.Workspace.get_window(request.second_window)
    dock_position = ui.DockPosition.__members__.get(request.dock_position.upper())
    
    # Collect validation errors
    errors = []
    valid_info = []
    
    # Check if first window exists
    if win_to_be_docked is None:
        errors.append(f"first_window '{request.first_window}' not found")
    else:
        valid_info.append(f"first_window '{request.first_window}' is valid")
    
    # Check if second window exists
    if win_to_dock_into is None:
        errors.append(f"second_window '{request.second_window}' not found")
    else:
        valid_info.append(f"second_window '{request.second_window}' is valid")
    
    # Check if dock position is valid
    if dock_position is None:
        valid_positions = list(ui.DockPosition.__members__.keys())
        errors.append(f"dock_position '{request.dock_position}' is invalid (valid positions: {', '.join(valid_positions)})")
    else:
        valid_info.append(f"dock_position '{request.dock_position}' is valid")
    
    # If there are any errors, raise HTTPException with comprehensive message
    if errors:
        error_msg = "Bad request - " + "; ".join(errors)
        if valid_info:
            error_msg += ". Valid parameters: " + "; ".join(valid_info)
        logger.error(error_msg)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    
    win_to_be_docked.dock_in(win_to_dock_into, dock_position)
    msg = f"{request.first_window} docked into {request.second_window} with dock position as {request.dock_position}"
    logger.info(msg)
    return MessageResponse(message=msg)


@router.get("/window_dimensions/", response_model=Dict[str, float], tags=["Window"])
async def window_dimensions(window_name: str):
    """
    Retrieves the dimensions of the specified window.

    Parameters:
    
        window_name (str): The name of the window to retrieve the dimensions for.

    Returns:
    
        Dict[str, float]: A dictionary containing the following keys:
            - width (float): The width of the window.
            - height (float): The height of the window.
            - position_x (float): The x-coordinate of the window's top-left corner.
            - position_y (float): The y-coordinate of the window's top-left corner.

    Raises:
    
        HTTPException(404): If the specified window is not found.
    """
    windows = ui.Workspace.get_windows()
    window_list = []
    for window in windows:
        if window.title == window_name:
            window_list.append(window)
    try:
        if len(window_list) == 1:
            window = window_list[0]
        else:
            logger.warn(
                'Found %d windows named "%s". Using first visible window found',
                len(window_list),
                _encode_for_logging(window_name)
            )
            window = None
            for win in window_list:
                if win.visible:
                    window = win
                    break
        if window:
            height = window.height
            width = window.width
            position_x = window.position_x
            position_y = window.position_y
            return {
                "width": width,
                "height": height,
                "position_x": position_x,
                "position_y": position_y,
            }
        else:
            msg = f'Failed to find visible window: "{window_name}"'
            logger.error("%s: %s", LOG_WINDOW_NOT_FOUND, _encode_for_logging(window_name))
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
    except Exception:
        msg = f'Error occured while fetching dimensions of window: "{window_name}"'
        logger.error("%s: %s", LOG_WINDOW_DIMENSIONS, _encode_for_logging(window_name))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)


@router.get("/app_window_dimension/", response_model=Dict[str, Union[int, float]], tags=["Window"])
async def app_win_dimension() -> Dict[str, Union[int, float]]:
    """
        Get the dimensions of the application window and the main window.

    This endpoint retrieves the dimensions of the application window and the main window.
    
    Note: Returns zero values if the app window is minimized.

    Returns:
    
        Dict[str, Union[int, float]]: A dictionary containing the dimensions of the application window and the main window.

    Raises:
    
        HTTPException(404): If unable to get dimensions.
    """
    import omni.appwindow

    app_width = 0
    app_height = 0
    main_win_width = 0
    main_win_height = 0

    try:
        win = omni.appwindow.get_default_app_window()
        app_width = win.get_width()
        app_height = win.get_height()
        main_win_width = ui.Workspace.get_main_window_width()
        main_win_height = ui.Workspace.get_main_window_height()
        message = f"App dimension {app_width}x{app_height} Main window dimension {main_win_width}x{main_win_height}"
        logger.info(message)
        return {
            "app_width": app_width,
            "app_height": app_height,
            "main_win_width": main_win_width,
            "main_win_height": main_win_height,
        }
    except Exception:
        msg = "Unable to get app window and main window dimensions."
        logger.error(msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg
        )
