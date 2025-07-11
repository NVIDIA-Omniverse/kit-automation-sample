# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.


import html
import logging
import base64
from typing import List

import omni.kit.ui_test as ui_test
from fastapi import HTTPException, status
from omni.services.core import routers

from ..api_models.query_models import (
    FindElementRequest,
    FindElementResponse,
    FindElementsRequest,
    FindElementsResponse,
)
from ..utils.element_cache import element_cache
from ..utils.omnielement import OmniElement

logger = logging.getLogger("omni.kit.test.automation.sample")

router = routers.ServiceAPIRouter()

# Constants for log messages to avoid user-controlled data in format strings
LOG_PROPERTIES_SUCCESS = "Successfully fetched element properties for element ID"
LOG_PROPERTIES_FAILED = "Failed to fetch properties for widget with ID"


def _encode_for_logging(text: str) -> str:
    """Safely encode user-controlled text for logging."""
    if text.isalnum():
        return text
    return f"(encoded){base64.b64encode(text.encode('UTF-8')).decode('UTF-8')}"


@router.post(
    "/find_element/",
    response_model=FindElementResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    tags=["Query"],
)
async def find_element(request: FindElementRequest):
    """
        Find an element in the UI using a locator.

    This endpoint finds an element in the UI using a locator and returns its ID. If the element already exists in the cache, its ID is returned directly.

    Parameters:

        request (FindElementRequest): The request object containing the locator and the root widget ID.
            - locator (str): The locator to use for finding the element.
            - root_widget_id (Optional[str]): The ID of the root widget to use for searching for the element. If not provided, the entire UI will be searched.

    Returns:

        FindElementResponse: A response object containing the following attributes:
            - element_id (Optional[str]): The ID of the found element, or None if no element was found.
            - message (str): A message indicating the result of the search.
            - properties (Optional[Dict]): A dictionary of properties of the found element, or None if no element was found.

    Raises:

        HTTPException: If the request is invalid or the element could not be found.
    """
    element: OmniElement = None

    if request.root_widget_id:
        try:
            root_widget: OmniElement = element_cache.get_cached_element(
                request.root_widget_id
            )
            element = root_widget.find_all(request.locator)
        except KeyError:
            logger.error(f"No root elements found with ID {request.root_widget_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No root elements found with ID {request.root_widget_id}",
            )
    else:
        element = ui_test.find_all(request.locator)

    if element:
        identifier = element_cache.add_element(element[0])

        if request.root_widget_id:
            message = f"Element with locator '{request.locator}' and root widget {root_widget.realpath} found and cached with ID '{identifier}'"
        else:
            message = f"Element with locator '{request.locator}' found and cached with ID '{identifier}'"

        logger.info(message)

    else:
        logger.error(f"No elements found with path {request.locator}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No elements found with locator '{request.locator}'",
        )

    return FindElementResponse(
        element_id=identifier,
        message=message,
        properties=element_cache.get_cached_element(identifier).get_properties(),
    )


@router.post(
    "/find_elements/",
    response_model=FindElementsResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    tags=["Query"],
)
async def find_elements(request: FindElementsRequest):
    """
        Find multiple elements in the UI using a locator.

    This endpoint finds multiple elements in the UI using a locator and returns their IDs. If the elements already exist in the cache, their IDs are returned directly.

    Parameters:

        request (FindElementsRequest): The request object containing the locator, root widget ID, and whether to return properties.
            - locator (str): The locator to use for finding the elements.
            - root_widget_id (Optional[str]): The ID of the root widget to use for searching for the elements. If not provided, the entire UI will be searched.
            - get_properties (bool): Whether to return a dictionary of properties for each found element. Defaults to True.

    Returns:

        FindElementsResponse: A response object containing the following attributes:
            - elements (List[FindElementResponse]): A list of FindElementResponse objects representing the found elements, or an empty list if no elements were found.
            - count (int): The number of elements found.

    Raises:

        HTTPException: If the request is invalid or no elements could be found.
    """
    element_list: List[OmniElement] = []

    if request.root_widget_id:
        try:
            root_widget: OmniElement = element_cache.get_cached_element(
                request.root_widget_id
            )
            element_list = root_widget.find_all(request.locator)
        except KeyError:
            logger.error(f"No root elements found with ID {request.root_widget_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No root elements found with ID {request.root_widget_id}",
            )
    else:
        element_list = ui_test.find_all(request.locator)

    response_list = []

    if len(element_list) < 50:
        exists_check = True
    else:
        exists_check = False
    logger.warn(f"Caching check set to {exists_check}")
    for element in element_list:
        identifier = element_cache.add_element(element, exists_check=exists_check)

        if request.root_widget_id:
            message = f"Element with locator '{request.locator}' and root widget '{root_widget.path}' found and cached with ID '{identifier}'"
        else:
            message = f"Element with locator '{request.locator}' found and cached with ID '{identifier}'"

        logger.info(message)

        (
            response_list.append(
                FindElementResponse(
                    element_id=identifier,
                    message=message,
                    properties=element_cache.get_cached_element(
                        identifier
                    ).get_properties(),
                )
            )
            if request.get_properties
            else response_list.append(
                FindElementResponse(
                    element_id=identifier,
                    message=message,
                    properties=None
                )
            )
        )

    if not element_list:
        logger.error(f"No elements found with path {request.locator}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No elements found with locator '{request.locator}'",
        )

    return FindElementsResponse(elements=response_list, count=len(response_list))


@router.get(
    "/context_menu_tree/",
    status_code=status.HTTP_200_OK,
    tags=["Query"],
)
async def context_menu_tree():
    """
        Get the context menu tree.

    This endpoint fetches the context menu tree and returns it as a dictionary. If the context menu cannot be found or is not visible, an error message is returned.

    Returns:

        Dict[str, Union[Dict, str]]: A dictionary containing the context menu tree or an error message.

    Raises:

        HTTPException: If the context menu could not be found or was not visible.
    """
    try:
        menu_tree = await ui_test.get_context_menu()
        return menu_tree
    except Exception as e:
        message = str(e)
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)


def find_context_menu_item(query, menu_root):
    """
        Find a context menu item by its name in the context menu tree.

    Parameters:
        query (str): The name of the context menu item to find.
        menu_root (OmniElement): The root menu of the context menu tree.

    Returns:
        Optional[OmniElement]: The found context menu item or None if not found.
    """
    import re

    from omni import ui

    def find_menu_item(query, menu_root):
        menu_items = ui.Inspector.get_children(menu_root)
        for menu_item in menu_items:
            if isinstance(menu_item, ui.MenuItem) or isinstance(menu_item, ui.Menu):
                name = re.sub(r"[^\x00-\x7F]+", " ", menu_item.text).lstrip()
                if query == name:
                    return menu_item
        return None

    tokens = query.split("/")
    child = menu_root
    for i in range(0, len(tokens)):
        token = tokens[i]
        child = find_menu_item(token, child)
        if not child:
            break
    return child


@router.get(
    "/widget_properties/",
    response_model=FindElementResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    tags=["Query"],
)
async def widget_properties(element_id: str):
    """
        Retrieves the widget property of a queried widget using it's unique identifier

    Parameters:

        element_id (str): The ID of the widget to use for searching for the element's properties.

    Returns:

        FindElementResponse: A response object containing the following attributes:
            - element_id (Optional[str]): The ID of the found element, or None if no element was found.
            - message (str): A message indicating the result of the search.
            - properties (Optional[Dict]): A dictionary of properties of the found element, or None if no element was found.

    Raises:

        HTTPException: If the request is invalid or the element could not be found.
    """
    try:
        properties = element_cache.get_cached_element(element_id).get_properties()
        message = "Successfully fetched element properties"
        element_id_escaped = html.escape(element_id)
        encoded_id = _encode_for_logging(element_id_escaped)
        logger.info("%s: %s", LOG_PROPERTIES_SUCCESS, encoded_id)

    except Exception as e:
        element_id_escaped = html.escape(element_id)
        encoded_id = _encode_for_logging(element_id_escaped)
        logger.error("%s: %s. Error: %s", LOG_PROPERTIES_FAILED, encoded_id, str(e))

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No elements found with ID {element_id}",
        )
    return FindElementResponse(
        element_id=element_id, message=message, properties=properties
    )
