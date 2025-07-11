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


class ViewportScreenshotRequest(BaseModel):
    """
    Model representing a request to take a screenshot of a web page's viewport.

    Attributes:

        dir (str): The directory where the screenshot will be saved.
    """

    dir: str


class ViewportScreenshotResponse(BaseModel):
    """
    Model representing the response from a viewport screenshot request.

    Attributes:

        file_path (str): The path to the saved screenshot file.
        message (str): A message describing the result of the request.
    """

    file_path: str = ""
    message: str


class ZoomViewportRequest(BaseModel):
    """
    Model representing a request to zoom in or out of a web page's viewport.

    Attributes:

        direction (str): The direction of the zoom. Can be 'IN' or 'OUT'.
        x (float): The x-coordinate of the point to zoom in/out around.
        y (float): The y-coordinate of the point to zoom in/out around.

    Config:

        json_schema_extra (Dict): Additional schema metadata for the request model.

    """

    direction: str
    x: float
    y: float

    class Config:
        """Configuration for the request model"""

        json_schema_extra = {
            "example": {
                "direction": "IN",
                "x": 100,
                "y": 500,
            }
        }


class CoordinateViewportRequest(BaseModel):
    """
    Model representing a request to move the viewport to specific coordinates.

    Attributes:

        x (float): The x-coordinate to move the viewport to.
        y (float): The y-coordinate to move the viewport to.

    Config:

        json_schema_extra (Dict): Additional schema metadata for the request model.

    """

    x: float
    y: float

    class Config:
        """Configuration for the request model"""

        json_schema_extra = {
            "example": {
                "x": 100,
                "y": 500,
            }
        }


class CameraSettingsResponse(BaseModel):
    """
    Model representing the camera settings response.

    Attributes:

        camera_path (str): The path to the camera.
        speed (dict, optional): The camera speed settings.
        exposure (dict, optional): The camera exposure settings.
        lens (dict, optional): The camera lens settings.
    """

    camera_path: str
    speed: Optional[dict] = None
    exposure: Optional[dict] = None
    lens: Optional[dict] = None
