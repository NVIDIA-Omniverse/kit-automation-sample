# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.


from typing import List

from pydantic import BaseModel


class WindowListResponse(BaseModel):
    """
    Model representing a list of visible and all application windows.

    Attributes:
    
        visible_windows (List[str]): A list of paths to the visible application
            windows.
        all_windows (List[str]): A list of paths to all application windows.
    """

    visible_windows: List[str]
    all_windows: List[str]


class DockWindowRequest(BaseModel):
    """
    Model representing a request to dock one window to another.

    Attributes:
    
        first_window (str): The path to the first window.
        second_window (str): The path to the second window.
        dock_position (str): The position to dock the first window to the
            second window. Can be 'LEFT', 'RIGHT', 'TOP', or 'BOTTOM'.
    """

    first_window: str
    second_window: str
    dock_position: str


class ResizeWindowRequest(BaseModel):
    """
    Model representing a request to resize a window.

    Attributes:
    
        id (str): The ID of the window to resize.
        new_width (float): The new width of the window.
        new_height (float): The new height of the window.
    """

    id: str
    new_width: float
    new_height: float
