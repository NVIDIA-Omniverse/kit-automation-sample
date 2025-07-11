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


class ContextMenuRequest(BaseModel):
    """
    Model representing a request to show a context menu.

    Attributes:
    
        path (str): The path of the menu item to show the context menu for,
            separated by '/'.
        offset_x (int, optional): The horizontal offset of the context menu.
            Defaults to 50.
        offset_y (int, optional): The vertical offset of the context menu.
            Defaults to 0.
        human_delay_speed (int, optional): The delay speed in milliseconds
            between key presses to simulate human-like typing. Defaults to 10.
    """

    path: str
    offset_x: Optional[int] = 50
    offset_y: Optional[int] = 0
    human_delay_speed: Optional[int] = 10


class MenuClickRequest(BaseModel):
    """
    Model representing a request to click a menu item.

    Attributes:
    
        path (str): The path of the menu item to click, separated by '/'.
    """

    path: str
