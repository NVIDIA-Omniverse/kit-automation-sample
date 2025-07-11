# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.


from pydantic import BaseModel


class ScreenshotResponse(BaseModel):
    """
    Model representing a response for a screenshot request.

    Attributes:
    
        file_path (str): The path to the saved screenshot image.
        message (str): The response message.
    """

    file_path: str = ""
    message: str


class ScreenshotRequest(BaseModel):
    """
    Model representing a request to take a screenshot.

    Attributes:
    
        dir (str): The directory where the screenshot image will be saved.
    """

    dir: str


class StageLoadRequest(BaseModel):
    """
    Model representing a request to load a stage.

    Attributes:
    
        frames (int): Max number of frames to load.
        seconds (int): Max number of seconds to load.
    """

    frames: int
    seconds: int
