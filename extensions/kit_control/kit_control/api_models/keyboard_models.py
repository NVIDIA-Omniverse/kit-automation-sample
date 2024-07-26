# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.


from typing import Optional

from pydantic import BaseModel


class SendKeysRequest(BaseModel):
    """
    Model representing a send keys request.

    Attributes:
    
        element_id (str): The ID of the element to send keys to.
        text (str): The text to be sent.
        human_delay_speed (int, optional): The delay speed in milliseconds
            between key presses to simulate human-like typing. Defaults to 20.
    """

    element_id: str
    text: str
    human_delay_speed: Optional[int] = 20


class KeyPressRequest(BaseModel):
    """
    Model representing a key press request.

    Attributes:
    
        combo (str): The key combination to be pressed.
        hold (bool): A boolean value indicating whether to hold the keys or
            not.
        release (bool): A boolean value indicating whether to release the
            keys or not.
        hold_duration (int, optional): The duration in seconds to hold the
            keys. Defaults to 5.
    """

    combo: str
    hold: bool
    release: bool
    hold_duration: int = 5
