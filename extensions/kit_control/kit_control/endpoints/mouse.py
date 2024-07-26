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

import omni.kit.ui_test as ui_test
from carb.input import MouseEventType
from fastapi import HTTPException, status
from omni import ui
from omni.kit.ui_test.vec2 import Vec2
from omni.services.core import routers

from ..api_models.common_models import MessageResponse
from ..api_models.mouse_models import (
    ClickAt,
    ClickHold,
    ClickRequest,
    DragDropRequestModel,
    DragFromDropToRequestModel,
    MouseMove,
    ScrollRequestModel,
)
from omni.kit.ui_test.input import human_delay
from ..utils.element_cache import element_cache
from ..utils.omnielement import OmniElement

logger = logging.getLogger("kit_control")

router = routers.ServiceAPIRouter()


@router.post(
    "/click/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Mouse Operations"],
)
async def click(request: ClickRequest):
    """
        Clicks on an element in the UI.

    This endpoint sends click events to an element in the UI and returns a response indicating success or failure.

    `Note`:

        Clicking on OmniUI window is not valid, click events can only be sent to a widget.

    Parameters:

        request (ClickRequest): The request object containing the click parameters.
            - element_id (str): The ID of the element to click on.
            - bring_to_front (bool): Whether to bring the element to the front of the UI before clicking.

    Returns:

        MessageResponse: A dictionary containing the message.

    Raises:

        HTTPException: If the request is invalid or the element could not be found.
    """
    try:
        element: OmniElement = element_cache.get_cached_element(request.element_id)
        if len(element.path.split("/")) == 1:
            raise RuntimeError(
                f"Clicking on OmniUI window is not valid, try clicking on a widget instead. Path of window: {element.path}"
            )
        await element.click(bring_to_front=request.bring_to_front)
        message = f"Click event has been sent to element with identifier {request.element_id} at path {element.realpath}"
        logger.info(message)
        return MessageResponse(message=message)
    except KeyError:
        msg = f"Element with identifier {request.element_id} not found"
        logger.error(msg)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
    except Exception as e:
        if "OmniUI window" in str(e):
            logger.error(str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
        else:
            logger.error(
                f"Click event not sent to Element with ID {request.element_id}: {str(e)}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Click event not sent to Element with ID {request.element_id}: {str(e)}",
            )


@router.post(
    "/double_click/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Mouse Operations"],
)
async def double_click(request: ClickRequest):
    """
        Double Clicks on an element in the UI.

    This endpoint sends double click events to an element in the UI and returns a response indicating success or failure.

    `Note`:

        Clicking on OmniUI window is not valid, click events can only be sent to a widget.

    Parameters:

        request (ClickRequest): The request object containing the double click parameters.
            - element_id (str): The ID of the element to double click on.
            - bring_to_front (bool, optional): Whether to bring the element to the front before double clicking. Defaults to True.

    Returns:

        MessageResponse: A dictionary containing the message.

    Raises:
        HTTPException: If the request is invalid or the element could not be found.
    """
    try:
        element: OmniElement = element_cache.get_cached_element(request.element_id)
        if len(element.path.split("/")) == 1:
            raise RuntimeError(
                f"Clicking on OmniUI window is not valid, try clicking on a widget instead. Path of window: {element.path}"
            )
        await element.double_click()
        message = f"Double Click event has been sent to element with identifier {request.element_id} at path {element.realpath}"
        logger.info(message)
        return MessageResponse(message=message)
    except KeyError:
        msg = f"Element with identifier {request.element_id} not found"
        logger.error(msg)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
    except Exception as e:
        if "OmniUI window" in str(e):
            logger.error(str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
        else:
            logger.error(
                f"Double Click event not sent to Element with ID {request.element_id}: {str(e)}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
            )


@router.post(
    "/right_click/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Mouse Operations"],
)
async def right_click(request: ClickRequest):
    """
        Right Clicks on an element in the UI.

    This endpoint sends right click events to an element in the UI and returns a response indicating success or failure.

    `Note`:

        Clicking on OmniUI window is not valid, click events can only be sent to a widget.

    Parameters:

        request (ClickRequest): The request object containing the right click parameters.
            - element_id (str): The ID of the element to right click on.
            - bring_to_front (bool, optional): Whether to bring the element to the front before right clicking. Defaults to True.

    Returns:

        MessageResponse: A dictionary containing the message.

    Raises:

        HTTPException: If the request is invalid or the element could not be found.
    """
    try:
        element: OmniElement = element_cache.get_cached_element(request.element_id)
        if len(element.path.split("/")) == 1:
            raise RuntimeError(
                f"Clicking on OmniUI window is not valid, try clicking on a widget instead. Path of window: {element.path}"
            )
        await element.right_click()
        message = f"Right Click event has been sent to element with identifier {request.element_id} at path {element.realpath}"
        logger.info(message)
        return MessageResponse(message=message)
    except KeyError:
        msg = f"Element with identifier {request.element_id} not found"
        logger.error(msg)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
    except Exception as e:
        if "OmniUI window" in str(e):
            logger.error(str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
        else:
            logger.error(
                f"Right Click event not sent to Element with ID {request.element_id}: {str(e)}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
            )


@router.post(
    "/drag_and_drop/",
    status_code=status.HTTP_201_CREATED,
    response_model=MessageResponse,
    tags=["Mouse Operations"],
)
async def drag_and_drop(request: DragDropRequestModel):
    """
        Drag and drop an element to a specific position.

    This endpoint allows the user to drag and drop an element to a specific position on the screen.
    The endpoint expects a `DragDropRequestModel` as input, which contains the ID of the element to be
    dragged and dropped, as well as the x and y coordinates of the destination position.

    Parameters:

        request (DragDropRequestModel): The request model containing the ID of the element to be dragged
            and dropped, as well as the x and y coordinates of the destination position.

            - element_id (str): The ID of the element to drag and drop.
            - xpos (float): The x-coordinate of the position to drop the element.
            - ypos (float): The y-coordinate of the position to drop the element.

    Returns:

        MessageResponse: A response model containing a message indicating that the element was
            successfully dragged and dropped.

    Raises:

        HTTPException: If the element with the given ID is not found, a 404 Not Found exception is raised.
        HTTPException: If an unexpected error occurs while dragging and dropping the element, a 500
            Internal Server Error exception is raised.
    """
    try:
        element: OmniElement = element_cache.get_cached_element(request.element_id)
        await element.drag_and_drop(Vec2(request.xpos, request.ypos))
        msg = f"Element with ID {request.element_id} dragged and dropped to x:{request.xpos} y:{request.ypos}"
        logger.info(msg)
        return MessageResponse(message=msg)
    except KeyError:
        msg = f"Element with identifier {request.element_id} not found"
        logger.error(msg)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
    except Exception as e:
        logger.error(
            f"Drag Drop event not sent to Element with ID {request.element_id} at path {element.realpath}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.post(
    "/drag_from_and_drop_to/",
    status_code=status.HTTP_201_CREATED,
    response_model=MessageResponse,
    tags=["Mouse Operations"],
)
async def drag_from_and_drop_to(request: DragFromDropToRequestModel):
    """
        Endpoint to simulate a drag and drop event using mouse.

    This endpoint emulates a mouse drag and drop event using the provided
    coordinates involved in the operation.

    Parameters:

        request (DragFromDropToRequestModel): The request model containing the coordinates
            involved in the drag and drop operation.
            - `x_in` (int): The x-coordinate of the starting point of the drag event.
            - `y_in` (int): The y-coordinate of the starting point of the drag event.
            - `x_dest` (int): The x-coordinate of the destination point of the drop event.
            - `y_dest` (int): The y-coordinate of the destination point of the drop event.

    Returns:

        MessageResponse: A response object containing a message indicating the
            success or failure of the operation.

    Raises:

        HTTPException: An internal server error occurred while processing the
            request.
    """
    try:
        await ui_test.emulate_mouse_drag_and_drop(
            Vec2(request.x_in, request.y_in), Vec2(request.x_dest, request.y_dest)
        )
        msg = f"Mouse dragged from x:{request.x_in} y:{request.y_in} and dropped to x:{request.x_dest} y:{request.y_dest}"
        logger.info(msg)
        return MessageResponse(message=msg)
    except Exception as e:
        logger.error(f"Drag Drop event not sent: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.post(
    "/scroll_into_view/",
    status_code=status.HTTP_201_CREATED,
    response_model=MessageResponse,
    tags=["Mouse Operations"],
)
async def scroll_into_view(request: ScrollRequestModel):
    """
        Scrolls the element in the specified axis and scroll amount.

    `Note`:

        1. Certain windows like Property window behave differently for this API, the UI only gets updated once the mouse hovers over the window.
        2. This API doesn't work on windows which contains list of thumbnails like Materials, Assets, Sample Scene.

    Parameters:

        request (ScrollRequestModel): The request object containing the id of the element and the scroll amount.
            - element_id (str): The ID of the element to scroll.
            - axis (str): The axis to scroll on. Can be 'X' or 'Y'.
            - scroll_amount (float): The amount to scroll by. 0 brings the widget to top, 0.5 to middle and 1 to bottom of the window.

    Returns:

        MessageResponse: A response object containing the message.
    """
    try:
        element: OmniElement = element_cache.get_cached_element(request.element_id)
        if request.axis.lower() == "x":
            element.widget.scroll_here_x(request.scroll_amount)
        else:
            element.widget.scroll_here_y(request.scroll_amount)
        await ui_test.common.human_delay(5)
        update_cached_elements_after_scroll(element)
        msg = f"Scrolling in {request.axis} axis for {request.scroll_amount} amount for element at {element.realpath}"
        logger.info(msg)
        return MessageResponse(message=msg)
    except KeyError:
        msg = f"Element with identifier {request.element_id} not found"
        logger.error(msg)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)


def update_cached_elements_after_scroll(element: OmniElement):
    """
    Updates the coordinates of all cached elements after scrolling through the window.

    Parameters:

        element (OmniElement): The element to scroll.
    """
    scroll_window = element.path.split("/")[0]
    element_map = element_cache.get_map()
    for element_key, cached_element in element_cache.get_map().items():
        if (
            cached_element.path.split("/")[0] == scroll_window
            and cached_element.realpath is not None
        ):
            try:
                if isinstance(cached_element.widget, ui.ComboBox):
                    element_map[element_key] = OmniElement(
                        ui_test.find_all(cached_element.path)[0]
                    )
                else:
                    element_map[element_key] = OmniElement(
                        ui_test.find_all(
                            cached_element.realpath.replace("Frame[0]", "Frame[*]")
                        )[0]
                    )
            except Exception:
                element_list = ui_test.find_all(cached_element.path)
                if element_list:
                    element_map[element_key] = OmniElement(element_list[0])
    logger.info("Updated coordinates of all cached elements")


@router.post(
    "/mouse_move/",
    status_code=status.HTTP_201_CREATED,
    response_model=MessageResponse,
    tags=["Mouse Operations"],
)
async def mouse_move(request: MouseMove):
    """
        Moves mouse to a user specified location.

    Parameters:

        request (MouseMove): Request object for mouse move.
            - x (float): The x-coordinate of the new mouse position.
            - y (float): The y-coordinate of the new mouse position.

    Raises:

        HTTPException: An internal server error occurred while processing the
            request.

    Returns:

        MessageResponse: A response object containing a message indicating the
            success or failure of the operation.
    """
    try:
        await ui_test.emulate_mouse_move(Vec2(request.x, request.y))
        msg = f"Mouse was moved to {request.x,request.y}"
        logger.info(msg)
        return MessageResponse(message=msg)
    except Exception as e:
        logger.error(f"Mouse move failed : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.post(
    "/click_at/",
    status_code=status.HTTP_201_CREATED,
    response_model=MessageResponse,
    tags=["Mouse Operations"],
)
async def click_at(request: ClickAt):
    """
        Click at a user specified location.

    Parameters:

        request (ClickAt): Request object for click at.
            - x (float): The x-coordinate of the position to click.
            - y (float): The y-coordinate of the position to click.
            - right (bool, optional): Whether to click with the right mouse button.
                Defaults to False.
            - double (bool, optional): Whether to perform a double click. Defaults to
                False.

    Raises:

        HTTPException: An internal server error occurred while processing the
            request.

    Returns:

        MessageResponse: A response object containing a message indicating the
            success or failure of the operation.
    """
    try:
        await ui_test.emulate_mouse_move_and_click(
            pos=Vec2(request.x, request.y),
            right_click=request.right,
            double=request.double,
        )
        msg = f"Mouse clicked at {request.x,request.y}"
        logger.info(msg)
        return MessageResponse(message=msg)
    except Exception as e:
        logger.error(f"Mouse click at failed : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


async def send_mouse_event(
    hold: bool,
    release: bool,
    x: float,
    y: float,
    mouse_down: MouseEventType,
    mouse_up: MouseEventType,
):
    """
        Simulates a click event for the given mouse input.

    Simulates a click event for the given mouse input. If `hold` is True, only the click event will be
    sent. If `release` is True, only the click release event will be sent. Otherwise, both the click and
    release events will be sent.

    Parameters:

        mouse_down (MouseEventType): The mouse input to press.
        mouse_up (MouseEventType): The mouse input to release.
        hold (bool): If True, only the click event will be sent. Defaults to False.
        release (bool): If True, only the  release event will be sent. Defaults to False.
        x (float): The x-coordinate of the position to click.
        y (float): The y-coordinate of the position to click.

    Raises:

        ValueError: If both `hold` and `release` are True.
    """
    if hold and release:
        raise ValueError("Both `hold` and `release` cannot be True.")

    if hold:
        await ui_test.input.emulate_mouse(MouseEventType.MOVE, Vec2(x, y))
        await ui_test.input.emulate_mouse(mouse_down)
    elif release:
        await ui_test.input.emulate_mouse(mouse_up)
    else:
        await ui_test.input.emulate_mouse(MouseEventType.MOVE, Vec2(x, y))
        await ui_test.input.emulate_mouse(mouse_down)
        await human_delay(5)
        await ui_test.input.emulate_mouse(mouse_up)


@router.post(
    "/send_mouse_events/",
    status_code=status.HTTP_201_CREATED,
    response_model=MessageResponse,
    tags=["Mouse Operations"],
)
async def send_mouse_events(request: ClickHold):
    """
        Performs a mouse click-and-hold operation.

    This endpoint is used to perform a mouse click-and-hold operation. The request body should contain the coordinates
    (x, y) where the mouse should be clicked, the duration to hold the mouse button down (hold), and the duration to
    wait before releasing the mouse button (release). The endpoint supports both left and right mouse button clicks,
    which can be specified using the right parameter in the request body.

    Parameters:

        request (ClickHold): The request body containing the details of the mouse click operation to be performed.
            - x (float): The x-coordinate of the click location.
            - y (float): The y-coordinate of the click location.
            - right (bool): Whether the click was performed using the right mouse button.
            - hold (bool): Whether the mouse button should be held down after the click.
                Defaults to False.
            - release (bool): Whether the mouse button should be released after being held down.
                Defaults to False.

    Returns:

        MessageResponse: A response object containing a message indicating the
            success or failure of the operation.

    Raises:

        HTTPException: An internal server error occurred while processing the
            request.
    """
    try:
        (
            await send_mouse_event(
                hold=request.hold,
                release=request.release,
                x=request.x,
                y=request.y,
                mouse_down=MouseEventType.RIGHT_BUTTON_DOWN,
                mouse_up=MouseEventType.RIGHT_BUTTON_UP,
            )
            if request.right
            else await send_mouse_event(
                hold=request.hold,
                release=request.release,
                x=request.x,
                y=request.y,
                mouse_down=MouseEventType.LEFT_BUTTON_DOWN,
                mouse_up=MouseEventType.LEFT_BUTTON_UP,
            )
        )
        msg = f"Mouse Press Operation Performed - X:{request.x}, Y:{request.y}, Release:{request.release}, Hold:{request.hold}"
        logger.info(msg)
        return MessageResponse(message=msg)
    except Exception as e:
        logger.error(f"Mouse click at and hold failed : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
