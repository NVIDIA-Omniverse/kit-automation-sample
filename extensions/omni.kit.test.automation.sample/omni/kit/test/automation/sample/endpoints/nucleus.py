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
from typing import Dict, List
import base64

import omni.client as omniclient
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from omni.services.core import routers

from ..api_models.common_models import MessageResponse

# Constants for log messages to avoid user-controlled data in format strings
LOG_FILES_FETCHED = "Fetched list of files from path"
LOG_FILE_LIST_ERROR = "Error occurred while fetching list of files from path"
LOG_DELETE_RESULT = "Delete operation result"
LOG_FILE_NOT_FOUND = "File or folder not found at path"
LOG_FILE_DELETED = "File or folder deleted from path"
LOG_CREATE_FOLDER_RESULT = "Create folder operation result"
LOG_FOLDER_EXISTS = "Folder already exists"
LOG_FOLDER_CREATED = "Folder created at path"
LOG_FOLDER_CREATE_ERROR = "Folder creation failed"
LOG_CONNECTION_REMOVED = "Removed connection for url"
LOG_CONNECTION_ERROR = "Failed to remove connection"

router = routers.ServiceAPIRouter()


logger = logging.getLogger("omni.kit.test.automation.sample")


def _encode_path_for_logging(path: str) -> str:
    if path.replace('/', '').replace(':', '').replace('\\', '').isalnum():
        return path
    return f"(encoded){base64.b64encode(path.encode('UTF-8')).decode('UTF-8')}"

def _encode_url_for_logging(url: str) -> str:
    if url.replace(':', '').replace('/', '').replace('.', '').isalnum():
        return url
    return f"(encoded){base64.b64encode(url.encode('UTF-8')).decode('UTF-8')}"


@router.get("/list/", tags=["Nucleus"])
async def list(folder_path: str):
    """
        List contents of folder at given folder_path.

    Parameters:
    
        folder_path (str): Path of the folder to list.

    Returns:
    
        Dict[str, List[str]]: A dictionary containing the status code, message and list of files in the folder.
    """
    folder_contents = []

    try:
        omniclient_resp = await omniclient.list_async(folder_path)
        message = str(omniclient_resp[0])
        if message == "Result.OK":
            folder_contents = [
                current_data.relative_path for current_data in omniclient_resp[1]
            ]
            encoded_path = _encode_path_for_logging(folder_path)
            logger.info("%s", LOG_FILES_FETCHED)
            return {"message": message, "folder_contents": folder_contents}
        else:
            error_msg = LOG_FILE_LIST_ERROR
            encoded_path = _encode_path_for_logging(folder_path)
            logger.error("%s Error: %s", error_msg, message)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error listing files at path '{folder_path}': {message}"
            )

    except Exception as e:
        error_msg = LOG_FILE_LIST_ERROR
        encoded_path = _encode_path_for_logging(folder_path)
        logger.error("%s Error: %s", error_msg, str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing files at path '{encoded_path}': {str(e)}"
        )


@router.delete(
    "/delete_folder_or_file/",
    response_model=Dict[str, str],
    status_code=status.HTTP_200_OK,
    tags=["Nucleus"],
)
async def delete_folder_or_file(path: str):
    """
        Delete a folder or file.

    This endpoint deletes a folder or file located at the specified path. If the folder or file is not found,
    a 404 HTTP exception is raised.

    Parameters:
    
        path (str): The path to the folder or file to delete.

    Returns:
    
        Dict[str, str]: A dictionary with a message and the path where the folder or file was deleted.

    Raises:
    
        HTTPException: If the folder or file is not found.
    """
    import omni.client

    result = await omni.client.delete_async(path)
    encoded_path = _encode_path_for_logging(path)
    logger.info("%s: %s", LOG_DELETE_RESULT, result)
    if result.name == "ERROR_NOT_FOUND":
        logger.error("%s", LOG_FILE_NOT_FOUND)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File or folder not found at path: {encoded_path}"
        )
    else:
        logger.info("%s", LOG_FILE_DELETED)
        return JSONResponse({"message": f"File or folder deleted at path: {encoded_path}", "path": encoded_path})


@router.post(
    "/create_folder/",
    response_model=Dict[str, str],
    status_code=status.HTTP_201_CREATED,
    tags=["Nucleus"],
)
async def create_folder(path: str):
    """
    Create a new folder.

    This endpoint creates a new folder at the specified path. If the folder already exists, a warning message is
    logged. If the folder creation fails for any other reason, a 500 HTTP exception is raised.

    Parameters:
    
        path (str): The path where the new folder should be created.

    Returns:
    
        A dictionary with a message and the path where the folder was created.

    Raises:
    
        HTTPException: If the folder creation fails.

    """
    import omni.client

    try:
        result = await omni.client.create_folder_async(path)
        encoded_path = _encode_path_for_logging(path)
        logger.info("%s: %s", LOG_CREATE_FOLDER_RESULT, result)
        if result.name == "ERROR_ALREADY_EXISTS":
            msg = f"Folder already exists at path: {path}"
            logger.warning("%s", LOG_FOLDER_EXISTS)
        else:
            logger.info("%s", LOG_FOLDER_CREATED)
            msg = f"Folder created at path: {path}"
        return JSONResponse({"message": msg, "path": encoded_path})

    except Exception as e:
        logger.error("%s: %s", LOG_FOLDER_CREATE_ERROR, str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=LOG_FOLDER_CREATE_ERROR % str(e)
        )


@router.get(
    "/remove_nucleus_connection/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Nucleus"],
)
async def remove_server_connections(url: str):
    """Removes nucleus server connection

    Parameters:
    
        url (str): Nuclues server url

    Returns:
    
        MessageResponse: A response object containing a message about the operation.

    Raises:
    
        HTTPException: Raises Exception If the operation Fails.

    """
    try:
        omniclient.sign_out(url=url)
        encoded_url = _encode_url_for_logging(url)
        logger.info("%s", LOG_CONNECTION_REMOVED)
        return JSONResponse({"message": f"Removed connection for url: {encoded_url}"})

    except Exception as e:
        encoded_url = _encode_url_for_logging(url)
        logger.error("%s. Error: %s", LOG_CONNECTION_ERROR, str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to remove connection for url '{encoded_url}': {str(e)}"
        )
