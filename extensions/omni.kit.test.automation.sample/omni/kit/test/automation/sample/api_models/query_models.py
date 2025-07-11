# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.


from typing import Dict, List, Optional

from pydantic import BaseModel


class FindElementResponse(BaseModel):
    """
    Model representing the response from finding an element.

    Attributes:

        element_id (Optional[str]): The ID of the found element, or None if no element was found.
        message (str): A message indicating the result of the search.
        properties (Optional[Dict]): A dictionary of properties of the found element, or None if no element was found.
    """

    element_id: Optional[str]
    message: str
    properties: Optional[Dict] = None

    class Config:
        json_encoders = {
            # Add any custom JSON encoders if needed
        }
        exclude_none = True


class FindElementRequest(BaseModel):
    """
    Model representing a request to find an element in a UI.

    Attributes:

        locator (str): A string in the format type=value used to search for the element.
        root_widget_id (Optional[str]): The ID of the root widget, if searching within a specific widget tree. Defaults to None.
    """

    locator: str
    root_widget_id: Optional[str] = None


class FindElementsRequest(BaseModel):
    """
    Model representing a request to find multiple elements in a UI.

    Attributes:

        locator (str): A string in the format type=value used to search for the elements.
        root_widget_id (Optional[str]): The ID of the root widget, if searching within a specific widget tree. Defaults to None.
        get_properties (bool): Whether to return a dictionary of properties for each found element. Defaults to True.
    """

    locator: str
    root_widget_id: Optional[str] = None
    get_properties: bool = True


class FindElementsResponse(BaseModel):
    """
    Model representing the response from finding multiple elements in a UI.

    Attributes:

        elements (List[FindElementResponse]): A list of FindElementResponse objects representing the found elements, or an empty list if no elements were found.
        count (int): The number of elements found.
    """

    elements: List[FindElementResponse]
    count: int

    class Config:
        json_encoders = {
            # Add any custom JSON encoders if needed
        }
        exclude_none = True
