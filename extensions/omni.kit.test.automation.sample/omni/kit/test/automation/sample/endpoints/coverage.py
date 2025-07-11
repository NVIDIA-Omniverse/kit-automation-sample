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
import os

import carb
import coverage
from fastapi import status
from omni.services.core import routers

from ..api_models.coverage_models import CoverageRequest, CoverageResponse

router = routers.ServiceAPIRouter()
settings = carb.settings.get_settings()
logger = logging.getLogger("omni.kit.test.automation.sample")

code_directory = []
code_directory.extend(settings.get("/app/exts/foldersCore"))
code_directory.extend(settings.get("/app/exts/folders"))
cov = coverage.Coverage(source=code_directory, branch=True)
coverage_location = os.path.join(os.path.expanduser("~"), "Coverage")
coverage_started = False


@router.post(
    "/coverage_endpoint/",
    response_model=CoverageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Coverage"],
)
async def code_coverage(request: CoverageRequest):
    """
        Perform code coverage for the app's extensions.

    This endpoint starts or stops code coverage analysis based on the provided boolean value.

    Parameters:

        action (bool): A boolean value to start or stop code coverage analysis. True starts the coverage and False stops the coverage.
        coverage_location (str, optional): A string value to specify the folder to store the coverage report. Defaults to a default path in Users dir.

    Returns:

        Dict[str,str]: A dictionary containing the following keys: -
            - 'message': A string describing the status of the operation.
            - 'html_report_path': The path to the coverage HTML report
            - 'coverage_percentage': Percent of code covered while the coverage calculation was being done.

    Raises:

        HTTPException: If the request is invalid or the code coverage could not be performed.
    """
    global coverage_started

    if request.action:
        if not coverage_started:
            cov.start()
            message = f"Code coverage started. Monitoring following paths - {', '.join(code_directory)}"
            logger.info(message)
            coverage_started = True
            return CoverageResponse(message=message)
        else:
            message = "Code coverage has already started"
            return CoverageResponse(message=message)
    else:
        if coverage_started:
            cov.stop()
            cov.save()

            html_report_path = (
                request.html_report_path
                if request.html_report_path
                else coverage_location
            )
            coverage_percentage = cov.html_report(directory=html_report_path)
            cov.save()
            coverage_started = False
            message = "Code coverage stopped and saved"
            logger.info(message)
            logger.info(f"HTML Coverage Report Path - {html_report_path}")
            logger.info(f"Coverage Percentage - {message}")
            return CoverageResponse(
                message=message,
                html_report_path=html_report_path,
                coverage_percentage=coverage_percentage,
            )
        else:
            message = "Code coverage has not started yet"
            return CoverageResponse(message=message)
