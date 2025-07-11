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
from typing import Dict, List, Union
import html
import base64
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from omni.services.core import routers

# Constants for log messages to avoid user-controlled data in format strings
LOG_EXTENSION_DETAILS = "Extension details type for ID"
LOG_EXTENSION_FETCH_ERROR = "Failed to fetch extension details for extension"

logger = logging.getLogger("omni.kit.test.automation.sample")

router = routers.ServiceAPIRouter()


@router.get(
    "/extension_list/", response_model=Dict[str, Union[List, int]], tags=["Extension"]
)
async def extension_list() -> Dict[str, Union[List, int]]:
    """
        This endpoint fetches and returns a dictionary containing the list of product extensions,
    the list of registry extensions, and the count of each.

    `WARNING`:

        This operation might time out if the list of available extensions is large.
    In such scenarios, it is recommended to use the 'extension_details' API instead.

    Returns:

        Dict[str, Union[List, int]]: A dictionary containing the following keys:
            - 'product_extensions': A list of installed product extensions.
            - 'registry_extensions': A list of registry extensions.
            - 'product_extensions_count': The count of installed product extensions.
            - 'registry_extensions_count': The count of registry extensions.

    Raises:

        HTTPException: If there's an error fetching the extensions.
    """

    import omni.kit.app

    try:
        ext_man = omni.kit.app.get_app().get_extension_manager()
        ext_list = ext_man.get_extensions()
        ext_man.sync_registry()
        ext_list_registry = ext_man.get_registry_extensions()
        msg = f"Product Extensions: {len(ext_list)}, Registry Extensions: {len(ext_list_registry)}"
        logger.info(msg)
        return {
            "extensions": ext_list,
            "registry_extensions": ext_list_registry,
            "product_extension_count": len(ext_list),
            "registry_extension_count": len(ext_list_registry),
        }
    except Exception as e:
        msg = f"Failed to fetch extensions. Error: {str(e)}"
        logger.error(msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg
        )


@router.get(
    "/extension_details", response_model=Dict[str, Union[str, Dict]], tags=["Extension"]
)
async def extension_details(ext_id: str):
    """
        This endpoint uses the OmniKit App Extension Manager to fetch the details of an extension.
    If the extension is found, it returns a dictionary containing the extension ID and its details.
    If the extension is not found or an error occurs during the fetching process,
    it raises an HTTPException with a 500 Internal Server Error status code.

    Parameters:

        ext_id (str): The unique identifier of the extension. It is in the format 'ext_name-version'.
            For example: 'omni.kit.ui_test-1.2.15', 'omni.kit.test.automation.sample-1.0.0'

    Returns:

        Dict[str, Union[str, Dict]]: A dictionary containing the following keys:
            - 'id': The unique identifier of the extension.
            - 'details': A dictionary containing the details of the extension.

    Raises:

        HTTPException: If the extension is not found or an error occurs during the fetching process.
    """
    import omni.kit.app

    ext_id_cleaned = html.escape(ext_id)
    try:
        ext_man = omni.kit.app.get_app().get_extension_manager()
        ext_details = (
            ext_man.get_extension_dict(ext_id_cleaned)
            if ext_man.get_extension_dict(ext_id_cleaned) is not None
            else ext_man.get_registry_extension_dict(ext_id_cleaned)
        )
        if ext_details is not None:
            ext_details = ext_details.get_dict()
            if ext_id_cleaned.isalnum():
                logger.info(LOG_EXTENSION_DETAILS + ": %s, type: %s", ext_id_cleaned, type(dict(ext_details)))
            else:
                encoded_id = base64.b64encode(ext_id_cleaned.encode('UTF-8')).decode('UTF-8')
                logger.info(LOG_EXTENSION_DETAILS + " (encoded): %s, type: %s", encoded_id, type(dict(ext_details)))
            return JSONResponse(
                {"ext_id": ext_id_cleaned, "extension_details": ext_details}
            )
        else:
            error_msg = LOG_EXTENSION_FETCH_ERROR
            if ext_id_cleaned.isalnum():
                logger.error(error_msg + ": %s", ext_id_cleaned)
            else:
                encoded_id = base64.b64encode(ext_id_cleaned.encode('UTF-8')).decode('UTF-8')
                logger.error(error_msg + " (encoded): %s", encoded_id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{error_msg}: {ext_id_cleaned}"
            )
    except HTTPException:
        # Re-raise HTTPException as-is to avoid recursive error messages
        raise
    except Exception as e:
        error_msg = LOG_EXTENSION_FETCH_ERROR
        if ext_id_cleaned.isalnum():
            logger.error(error_msg + ": %s. Error: %s", ext_id_cleaned, str(e))
        else:
            encoded_id = base64.b64encode(ext_id_cleaned.encode('UTF-8')).decode('UTF-8')
            logger.error(error_msg + " (encoded): %s. Error: %s", encoded_id, str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error_msg}: {ext_id_cleaned}. Error: {str(e)}"
        )
