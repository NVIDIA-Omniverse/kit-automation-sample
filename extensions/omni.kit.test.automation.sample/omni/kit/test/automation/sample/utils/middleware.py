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

from fastapi import Response
from omni.services.core import main


class CoreServices(main.ServicesCoreExtension):
    pass


logger = logging.getLogger("omni.kit.test.automation.sample")
core_services = CoreServices()


@core_services.app.middleware("http")
async def log_api(request, call_next):
    response = await call_next(request)
    body = b""
    async for chunk in response.body_iterator:
        body += chunk
    
    # Only log non-sensitive endpoints
    if "openapi.json" not in str(request.url) and "docs" not in str(request.url):
        # Log only method, path (not full URL), and status code
        logger.info(f"{request.method} {request.url.path}")
        logger.info(f"Status code: {response.status_code}")
        
        # Don't log request/response bodies as they may contain sensitive data
        if response.status_code >= 400:
            # Only log error messages for debugging, and let the SafeLogFilter handle encoding
            logger.error(f"Error response: {body.decode('utf-8', errors='replace')}")

    return Response(
        content=body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )
