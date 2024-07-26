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
import time
from typing import Dict, List

import omni.ui as ui
from fastapi import HTTPException, status
from omni.services.core import routers

from ..api_models.common_models import MessageResponse
from ..api_models.widget_models import (
    ComboBoxInfo,
    ComboBoxRequest,
)
from ..utils.element_cache import element_cache
from ..utils.omnielement import OmniElement

logger = logging.getLogger("kit_control")

router = routers.ServiceAPIRouter()


@router.delete("/widgets/cache/", tags=["Widget"])
async def reset_widget_cache() -> dict[str, str]:
    """
    Reset the server widget cache.

    Returns:

        dict: A success message if the cache was reset successfully.

    Raises:

        HTTPException: If the cache reset operation fails.
    """
    element_cache.reset_map()

    if element_cache.get_map():  # Check if the cache is still populated
        logger.error("Server cache reset operation failed.")
        raise HTTPException(
            status_code=500,
            detail={"message": "Server cache reset operation failed."},
        )

    logger.info("Server widget cache has been successfully reset.")
    return {"message": "Server widget cache has been successfully reset."}


@router.get("/combobox_info/", response_model=ComboBoxInfo, tags=["Widget"])
async def combobox_info(identifier: str):
    """
        Get information about a combobox widget.

    This endpoint retrieves information about a combobox widget based on the provided identifier.
    It retrieves the combobox model from the cached element and returns a `ComboBoxInfo` object containing information about the combobox.
    If the element with the provided identifier is not found, or if the item is not of type combobox, a 404 HTTP exception is raised.

    Parameters:

        identifier (str): The ID of the element containing the combobox.

    Returns:

        ComboBoxInfo: A request model containing the following information about the combobox:
            - current_value (str): The currently selected value in the combo box.
            - current_index (int): The index of the currently selected value.
            - all_options (List[str]): A list of all available options in the combo box.
            - options_count (int): The total number of options available in the combo box.

    Raises:
        HTTPException: If the element with the provided identifier is not found, or if the item is not of type combobox.
    """
    combobox_model = None

    try:
        element: OmniElement = element_cache.get_cached_element(identifier)
    except KeyError:
        msg = f"Element with ID {identifier} not found in element cache."
        logger.error(msg)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)

    try:
        combobox_model = element.model
    except Exception:
        try:
            combobox_model = element.widget.delegate._model
        except Exception as e:
            msg = f"Combobox model not found. Error: {str(e)}"
            logger.error(msg)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)

    try:
        string_items = combobox_model.get_item_children()
    except Exception:
        string_items = combobox_model.get_item_children(item=None)

    try:
        index = combobox_model.get_item_value_model(None, None).as_int
    except Exception:
        index = combobox_model.get_item_value_model().as_int

    value = combobox_model.get_item_value_model(string_items[index], 0).as_string
    items = []
    for i in string_items:
        items.append(combobox_model.get_item_value_model(i, 0).as_string)
    msg = (
        f"Found items in combobox {items}, current index {index}, current value {value}"
    )
    logger.info(msg)
    return ComboBoxInfo(
        current_index=index,
        current_value=value,
        all_options=items,
        options_count=len(items),
    )


@router.get("/bring_to_front/", response_model=MessageResponse, tags=["Widget"])
async def bring_to_front(id: str, undock: bool) -> MessageResponse:
    """
        Brings an element to the front of the screen, either docked or undocked.

    This endpoint brings an element to the front of the screen based on its unique identifier.
    The `undock` parameter determines whether the element should be undocked after being brought to the front.
    If the element is successfully brought to the front, a message is logged and returned.
    If the element with the given ID is not found in the element cache, a 404 HTTP exception is raised.

    Parameters:

        id (str): The unique identifier of the element to be brought to the front.
        undock (bool): Whether the element should be undocked after being brought to the front.

    Returns:

        MessageResponse: A response object containing a message indicating the success of the operation.

    Raises:

        HTTPException: If the element with the given ID is not found in the element cache.
    """
    try:
        element: OmniElement = element_cache.get_cached_element(id)
        await element.bring_to_front(undock)
        msg = f"Element with ID {id} brought to front with undock:{undock}"
        logger.info(msg)
        return MessageResponse(message=msg)
    except KeyError:
        msg = f"Element with ID {id} not found in element cache."
        logger.error(msg)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)


@router.post(
    "/select_combobox_item/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Widget"],
)
def select_combobox_item(request: ComboBoxRequest):
    """
        Selects an item from a combobox based on the provided index or name.

    This function retrieves the combobox model from the cached element using the provided identifier.
    It then attempts to select the item from the combobox based on the provided index or name.
    If the item is successfully selected, a message is logged and returned.
    If the item is not found, an error message is logged and a 404 HTTP exception is raised.

    `Note`:

        Use the GET `combobox_info` API to fetch all the available options.

    Parameters:

        request (ComboBoxRequest): The request containing the following parameters -
            - identifier (str): The identifier of the combo box to interact with.
            - index (int, optional): The index of the option to select.
            - name (str, optional): The name of the option to select.


    Returns:

        MessageResponse: A response containing a message indicating the success or failure of the operation.

    Raises:

        HTTPException: If the element with the provided identifier is not found, or if the item is not found in the combobox.
    """

    try:
        # Get the cached element using the identifier
        omni_element = element_cache.get_cached_element(request.identifier)
    except KeyError:
        # Log an error message and raise an HTTP exception if the element is not found
        message = f"Element with Identifier {request.identifier} not found"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    # Get the combobox model
    combobox_model = getattr(omni_element, "model", None) or getattr(
        omni_element.widget.delegate, "_model", None
    )

    if not combobox_model:
        message = f"Unable to fetch combobox model not found"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    try:
        # Get the string items in the combobox model
        string_items = combobox_model.get_item_children()
    except Exception:
        # Get the string items in the combobox model if the above fails
        string_items = combobox_model.get_item_children(item=None)

    str_index = request.index

    if str_index is None:
        str_index = next(
            (
                i
                for i, value in enumerate(string_items)
                if request.name
                == combobox_model.get_item_value_model(
                    item=value, column_id=None
                ).as_string
            ),
            len(string_items),
        )

    if str_index >= len(string_items):
        # Log an error message if the item is not found
        message = f"Item with name {request.name} and index {request.index} not present in combobox."
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    else:
        try:
            # Set the index of the combobox model
            combobox_model._current_index.as_int = str_index
        except Exception:
            try:
                combobox_model.get_item_value_model().as_int = str_index
            except Exception:
                # Set the index of the combobox model if the above fails
                combobox_model.get_item_value_model(
                    item=None, column_id=None
                ).as_int = str_index

        value = combobox_model.get_item_value_model(
            string_items[str_index], 0
        ).as_string

        # Log an info message
        message = f"Selected item at index {str_index} with value {value}."
        logger.info(message)
        return MessageResponse(message=message)
