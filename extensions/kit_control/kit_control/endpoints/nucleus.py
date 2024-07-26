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

import omni.client as omniclient
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from omni.services.core import routers

from ..api_models.common_models import MessageResponse

router = routers.ServiceAPIRouter()


logger = logging.getLogger("kit_control")


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
        omniclient_resp = omniclient.list(folder_path)
        message = str(omniclient_resp[0])
        if message == "Result.OK":
            folder_contents = [
                current_data.relative_path for current_data in omniclient_resp[1]
            ]
            logger.info(f"Fetched list of files from path: {folder_path}")
            return {"message": message, "folder_contents": folder_contents}
        else:
            msg = f"Error occurred while fetching list of files from path: {folder_path} Error:{str(message)}"
            logger.error(msg)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg
            )

    except Exception as e:
        msg = f"Error occurred while fetching list of files from path: {folder_path} Error:{str(e)}"
        logger.error(msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg
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

    result = omni.client.delete(path)
    logger.info(f"Delete operation result: {result}")
    if result.name == "ERROR_NOT_FOUND":
        msg = f"File or folder not found at path {path}"
        logger.error(msg)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
    else:
        msg = f"File or folder deleted from path {path}"
        logger.info(msg)
        return JSONResponse({"message": msg, "path": path})


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
        logger.info(f"Create folder operation result: {result}")
        if result.name == "ERROR_ALREADY_EXISTS":
            msg = f"Folder already exists."
            logger.warning(msg)
        else:
            msg = f"Folder created at path: {path}"
            logger.info(msg)
        return JSONResponse({"message": msg, "path": path})
    except Exception as e:
        msg = f"Folder creation failed due to {str(e)}"
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg
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
        logger.info(f"Removed connection for url: {url}")
        message = f"Removed connection for url: {url}"
        return JSONResponse({"message": message})

    except Exception as e:
        msg = f"Failed to remove connection from {url} due to {str(e)}"
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg
        )
