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


class ScrollRequestModel(BaseModel):
    """
    Model representing a request to scroll an element.

    Attributes:

        element_id (str): The ID of the element to scroll.
        axis (str): The axis to scroll on. Can be 'X' or 'Y'.
        scroll_amount (float): The amount to scroll by.
        0 brings the widget to top, 0.5 to middle and 1 to bottom of the window.

    Config:

        json_schema_extra (Dict): Additional schema metadata for the request model.
    """

    element_id: str
    axis: str
    scroll_amount: float

    class Config:
        """Configuration for the request model"""

        json_schema_extra = {
            "example": {
                "element_id": "b252968a-d0e6-46c6-a75e-13467f50ee37",
                "axis": "X",
                "scroll_amount": 0.5,
            }
        }


class ClickRequest(BaseModel):
    """
    Model representing a request to click on an element.

    Attributes:

        element_id (str): The ID of the element to click on.
        bring_to_front (bool, optional): Whether to bring the element to the
            front before clicking. Defaults to True.
    """

    element_id: str
    bring_to_front: Optional[bool] = True


class DragDropRequestModel(BaseModel):
    """
    Model representing a request to drag and drop an element to a position.

    Attributes:

        element_id (str): The ID of the element to drag and drop.
        xpos (float): The x-coordinate of the position to drop the element.
        ypos (float): The y-coordinate of the position to drop the element.

    Config:

        json_json_schema_extra (Dict): Additional schema metadata for the request model.
    """

    element_id: str
    xpos: float
    ypos: float

    class Config:
        """Configuration for the request model"""

        json_json_schema_extra = {
            "example": {
                "element_id": "12345",
                "xpos": 100,
                "ypos": 200,
            }
        }


class DragFromDropToRequestModel(BaseModel):
    """
    Model representing a request to drag an element from one position to
    another position.

    Attributes:

        x_in (float): The x-coordinate of the starting position of the drag.
        y_in (float): The y-coordinate of the starting position of the drag.
        x_dest (float): The x-coordinate of the ending position of the drag.
        y_dest (float): The y-coordinate of the ending position of the drag.

    Config:

        json_json_schema_extra (Dict): Additional schema metadata for the request model.
    """

    x_in: float
    y_in: float
    x_dest: float
    y_dest: float

    class Config:
        """Configuration for the request model"""

        json_json_schema_extra = {
            "example": {
                "x_in": 100,
                "y_in": 100,
                "x_dest": 200,
                "y_dest": 200,
            }
        }


class MouseMove(BaseModel):
    """
    Model representing a request to move the mouse cursor.

    Attributes:

        x (float): The x-coordinate of the new mouse position.
        y (float): The y-coordinate of the new mouse position.
    """

    x: float
    y: float


class ClickAt(BaseModel):
    """
    Model representing a request to click at a position.

    Attributes:

        x (float): The x-coordinate of the position to click.
        y (float): The y-coordinate of the position to click.
        right (bool, optional): Whether to click with the right mouse button.
            Defaults to False.
        double (bool, optional): Whether to perform a double click. Defaults to
            False.
    """

    x: float
    y: float
    right: bool = False
    double: bool = False


class ClickHold(BaseModel):
    """
    A model representing a click-hold-release event at a specific location.

    Attributes:

        x (float): The x-coordinate of the click location.
        y (float): The y-coordinate of the click location.
        right (bool): Whether the click was performed using the right mouse button.
        hold (bool): Whether the mouse button was held down after the click.
            Defaults to False.
        release (bool): Whether the mouse button was released after being held down.
            Defaults to False.

    Note:

        At least one of `hold` and `release` should be set to True to indicate
        that the mouse button was actually held and released.
    """

    x: float
    y: float
    right: bool
    hold: bool = False
    release: bool = False
