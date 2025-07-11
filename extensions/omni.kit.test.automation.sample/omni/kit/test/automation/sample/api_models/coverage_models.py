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


class CoverageRequest(BaseModel):
    """
    Model representing a request for generating a coverage report.

    Attributes:
    
        action (bool): A boolean value indicating whether to generate
            a coverage report or not.
        html_report_path (str, optional): The path to the HTML coverage
            report. Defaults to None.
    """

    action: bool
    html_report_path: Optional[str] = None


class CoverageResponse(BaseModel):
    """
    Model representing a response containing coverage report information.

    Attributes:
    
        message (str): The response message.
        html_report_path (str, optional): The path to the HTML coverage
            report. Defaults to None.
        coverage_percentage (float, optional): The percentage of code
            coverage. Defaults to None.
    """

    message: str
    html_report_path: Optional[str] = None
    coverage_percentage: Optional[float] = None
