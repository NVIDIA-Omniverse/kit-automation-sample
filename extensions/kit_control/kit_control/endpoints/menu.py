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
from typing import Dict, Optional

import omni.kit.ui_test as ui_test
from fastapi import HTTPException, status
from omni.services.core import routers

from ..api_models.menu_models import ContextMenuRequest, MenuClickRequest

logger = logging.getLogger("kit_control")

router = routers.ServiceAPIRouter()


@router.post(
    "/menu_select/",
    tags=["Menu"],
    response_model=Dict[str, str],
    status_code=status.HTTP_201_CREATED,
)
async def menu_select(request: MenuClickRequest):
    """
        Clicks on a menu item by path.

    This function clicks on a menu item by path. It returns a success message if the menu item is clicked successfully.

    Parameters:

        path (str): The path of the menu item, separated by `/` if nested. For example `File/Open`. Options needs to be put as displayed on UI, `case sensitive`.

    Returns:

        Dict[str, str]: A response dictionary containing the success message.
    """
    try:
        await ui_test.menu_click(request.path)
        message = f"Menu item with path {request.path} was clicked."
        logging.info(message)
        return {"message": message}
    except Exception as e:
        message = (
            f"Menu item with path {request.path} not found and clicked. Error: {str(e)}"
        )
        logging.error(message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
        )


@router.post(
    "/context_menu_select/",
    tags=["Menu"],
    response_model=Dict[str, str],
    status_code=status.HTTP_201_CREATED,
)
async def context_menu_select(request: ContextMenuRequest):
    """
        Selects an option from the context menu at the specified path and offset.

    This function selects an option from the context menu at the specified path and offset. It returns a success message if the option is selected successfully.

    `Note`:
    
        The right click should be done before calling this API to open the context menu, and then this API can select the options from it.

    Parameters:

        path (str): The path of the menu item, separated by `/` if nested. For example `Create/Mesh`. Options needs to be put as displayed on UI, `case sensitive`.
        offset_x (int, optional): The x offset of the context menu. Defaults to 50.
        offset_y (int, optional): The y offset of the context menu. Defaults to 0.
        human_delay_speed (int, optional): The delay speed in milliseconds between key presses to simulate human-like typing. Defaults to 10.

    Returns:

        Dict[str, str]: A response dictionary containing the success message.
    """
    try:
        await ui_test.select_context_menu(
            request.path,
            offset=ui_test.Vec2(request.offset_x, request.offset_y),
            human_delay_speed=request.human_delay_speed,
        )
        message = f"Context menu with path {request.path} was clicked with offset_x:({request.offset_x}, offset_y:{request.offset_y})."
        logger.info(message)
        return {"message": message}
    except Exception as e:
        message = f"Context menu with path {request.path} not found or could not be opened. Error: {str(e)}"
        logger.error(message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
        )


@router.get(
    "/live_menu_center", tags=["Menu"], response_model=Dict[str, Dict[str, int | float]]
)
async def live_menu_center():
    """
        Gets the center position of the "Live State Widget" button in the menubar.

    This function gets the center position of the `Live State Widget` button in the menubar and returns it as a dictionary. The keys of the dictionary are the x and y coordinates of the center position.

    Returns:

        Dict[str, Dict[str, int | float]]: A response dictionary containing the center position of the button.
    """
    try:
        menu_widget = ui_test.get_menubar()
        menu = menu_widget.find_menu("Live State Widget")
        button = menu.widget.delegate._live_button
        center = {
            "x": button.screen_position_x + button.computed_width / 2,
            "y": button.screen_position_y + button.computed_height / 2,
        }
        logger.info(f"Live button center: {center}")
        return {"Live Menu Center": center}
    except Exception as e:
        message = f"Failed to get live button center. Error: {str(e)}"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
