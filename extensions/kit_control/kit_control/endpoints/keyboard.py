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
from typing import Dict, List

from carb.input import KeyboardEventType, KeyboardInput
from fastapi import HTTPException, status
from omni.kit import ui_test
from omni.services.core import routers
from ..api_models.common_models import MessageResponse
from ..api_models.keyboard_models import (
    KeyPressRequest,
    SendKeysRequest,
)
from ..utils.element_cache import element_cache
from ..utils.omnielement import OmniElement

logger = logging.getLogger("kit_control")

router = routers.ServiceAPIRouter()


@router.post(
    "/send_keys_to_element/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Keyboard Operations"],
)
async def send_keys_to_element(request: SendKeysRequest):
    """
        This endpoint sends keys to a specific element in the UI and returns a response indicating success or failure.

    Parameters:

        element_id (str): The unique identifier of the element to send keys to.
        text (str): The text to be sent to the element.
        human_delay_speed (int, optional): The delay speed in milliseconds between key presses to simulate human-like typing. Defaults to 20.

    Returns:

        Dict[str, Union[str, int]]: A dictionary containing the following keys: -
            - 'message': A string describing the status of the operation.

    Raises:

        HTTPException: If the request is invalid or the element could not be found.
    """
    try:
        element: OmniElement = element_cache.get_cached_element(request.element_id)
        await element.input(request.text, human_delay_speed=request.human_delay_speed)
        result = True if element.text == request.text else False
    except KeyError:
        message = f"Element with Identifier {request.element_id} not found"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    if result:
        message = f"Keys '{request.text}' sent to Element with Identifier {request.element_id} and action validation passed."
        logger.info(message)
        return MessageResponse(message=message)
    else:
        message = f"{request.text} was sent to Element with Identifier {request.element_id} but action validation failed."
        logger.error(message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message,
        )


@router.post(
    "/send_keys/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Keyboard Operations"],
)
async def send_keys(text: str):
    """
        This endpoint emulates pressing a sequence of characters and returns a response indicating success or failure.

    Parameters:

        text (str): The sequence of characters to emulate pressing.

    Returns:

        MessageResponse: A dictionary containing the following keys:
            - 'message': A string describing the status of the operation.

    Raises:

        HTTPException: If the request is invalid or the characters could not be pressed.
    """

    try:
        await ui_test.emulate_char_press(text)
        message = f"Characters '{text}' pressed in sequence."
        logger.info(message)
    except Exception as e:
        message = f"Failed to press characters in sequence {text} due to {str(e)}."
        logger.error(message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message,
        )

    return MessageResponse(message=message)


@router.post(
    "/send_key_combo/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Keyboard Operations"],
)
async def send_key_combo(key_combo: str):
    """
       This endpoint sends a key combo to the UI and returns a response indicating success or failure.

    Key bindings need to be fetched from the `key_bindings` API.

    `Note`:
        For modifiers, use the format - `CTRL`, `SHIFT`, `ALT`

    Parameters:

        key_combo (str): The key combo to send to the element. Example - CTRL+A

    Returns:

        MessageResponse: A dictionary containing the following keys:
            - 'message': A string describing the status of the operation.

    Raises:

        HTTPException: If the request is invalid or the key combo could not be sent.
    """
    try:
        await ui_test.emulate_key_combo(key_combo)
        message = f"Key combo '{key_combo}' pressed."
        logger.info(message)
    except Exception as e:
        message = f"Failed to press key combo {key_combo} due to {str(e)}."
        logger.error(message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message,
        )

    return MessageResponse(message=message)


async def send_key_press(
    key: KeyboardInput,
    hold: bool = False,
    release: bool = False,
    hold_duration: int = 5,
):
    """
        Simulates a key press event for the given keyboard input.

    This function simulates a key press event for the given keyboard input. If hold is True, only the key press event will be sent.
    If release is True, only the key release event will be sent.
    Otherwise, both the key press and release events will be sent, with the key held down for hold_duration seconds.

    Parameters:

        key (KeyboardInput): The keyboard input to emulate.
        hold (bool): If True, only the key press event will be sent. Defaults to False.
        release (bool): If True, only the key release event will be sent. Defaults to False.
        hold_duration (int): The duration to hold the key down, in seconds. Only used if hold is False. Defaults to 5.

    Raises:

        ValueError: If both hold and release are True.
    """
    if hold and release:
        raise ValueError("Both `hold` and `release` cannot be True.")

    if hold:
        await ui_test.input.emulate_keyboard(KeyboardEventType.KEY_PRESS, key)
    elif release:
        await ui_test.input.emulate_keyboard(KeyboardEventType.KEY_RELEASE, key)
    else:
        await ui_test.input.emulate_keyboard(KeyboardEventType.KEY_PRESS, key)
        await asyncio.sleep(hold_duration)
        await ui_test.input.emulate_keyboard(KeyboardEventType.KEY_PRESS, key)


@router.post(
    "/send_key_events/",
    tags=["Keyboard Operations"],
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def key_events(request: KeyPressRequest):
    """
        Emulate pressing a key combo in the UI.

    This endpoint emulates pressing a key combo in the UI and returns a response indicating success or failure.

    Key bindings need to be fetched from the key_bindings API.

    `Note`:
     For modifiers, use the exact same values from the `key_bindings` API. No special rules like the key_combo API.

    Parameters:

        request (KeyPressRequest): The request containing the key combo, hold, release, and hold_duration parameters.

    Returns:

        MessageResponse: A dictionary containing the following keys:
            - 'message': A string describing the status of the operation.

    Raises:

        HTTPException: If the request is invalid or the key combo could not be pressed.
    """
    try:
        keys = request.combo.split("+")
        for key in keys:
            input_button = KeyboardInput.__members__.get(key)
            if input_button is None:
                raise ValueError(f"Invalid key: {key}")
            await send_key_press(
                input_button, request.hold, request.release, request.hold_duration
            )
            logger.info(
                f"Key Press Operation Performed - Key:{input_button}, Hold:{request.hold}, Release:{request.release}, Hold Duration:{request.hold_duration}"
            )
        message = f"Key combo '{request.combo}' pressed."
        logger.info(message)
        return MessageResponse(message=message)
    except Exception as e:
        message = f"Failed to press key combo {request.combo} due to {str(e)}."
        logger.error(message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message,
        )


@router.get(
    "/key_bindings/",
    tags=["Keyboard Operations"],
    response_model=Dict[str, List[str]],
    status_code=status.HTTP_200_OK,
)
def key_bindings():
    """
       Fetches the key bindings for the keyboard operations.

    This function fetches the key bindings for the keyboard operations and returns them as a dictionary.
    The keys of the dictionary are the names of the keyboard operations, and the values are lists of the key bindings for those operations.

    Returns:

        Dict[str, List[str]]: A dictionary containing the key bindings.

    Raises:

        HTTPException: If there is an error fetching the key bindings.
    """
    try:
        key_bindings = list(KeyboardInput.__members__.keys())
        logger.info("Fetched the key bindings.")
        return {"key_bindings": key_bindings}
    except Exception as e:
        message = f"Failed to fetch key bindings due to {str(e)}."
        logger.error(message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message,
        )
