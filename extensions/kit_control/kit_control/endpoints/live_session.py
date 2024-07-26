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

import omni.kit.ui_test as ui_test
from fastapi import HTTPException, status
from omni.services.core import routers

from ..api_models.common_models import MessageResponse
from ..api_models.live_session_models import *

logger = logging.getLogger("kit_control")

router = routers.ServiceAPIRouter()


def is_live_sync_enabled() -> bool:
    """
        Returns whether Live Sync is enabled or not in the UI.

    This function checks whether Live Sync is enabled in the UI and returns a boolean value indicating its status.

    Returns:

        bool: A boolean value indicating whether Live Sync is enabled in the UI.
    """
    menu_widget = ui_test.get_menubar()
    menu = menu_widget.find_menu("Live State Widget")
    return True if menu else False


@router.get(
    "/live_session_users/",
    response_model=Dict[str, Union[List, int]],
    tags=["Live Session"],
)
async def live_session_users():
    """
        Get the details of the current live session users.

    This function returns the list of users in the current live session.
    If the user is not in a live session, it raises an HTTPException with a 500 status code and a message indicating that the user is not in a live session.

    Returns:

        Dict[str, Union[List, int]]: A dictionary containing the list of users in the current live session.

    Raises:

        HTTPException: An exception with a 500 status code and a message indicating that the user is not in a live session.
    """

    if is_live_sync_enabled():
        import omni.kit.usd.layers as layers

        users = []
        live_sync = layers.get_live_syncing()
        curr_session = live_sync.get_current_live_session()
        if curr_session:
            users.append(curr_session.logged_user_name)
            users.extend(user.user_name for user in curr_session.peer_users)
            msg = f"Fetched live session users: {users}, Count: {len(users)}"
            logger.info(msg)
            return {"user_list": users, "count": len(users)}
        else:
            msg = "User is not in a Live Session"
            logger.error(msg)
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=msg)
    else:
        msg = "Live Session option is not enabled, please enable it and verify if Live Menu is visible on top right corner of the app."
        logger.error(msg)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)


@router.post(
    "/exit_live_session/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Live Session"],
)
async def exit_live_session():
    """
        Stop the current live session.

    This function stops the current live session and returns a success message.
    If the user is not in a live session, it raises an HTTPException with a 500 status code and a message indicating that the user is not in a live session.

    Returns:

        MessageResponse: A response object containing the success message.

    Raises:

        HTTPException: An exception with a 500 status code and a message indicating that the user is not in a live session.
    """
    if is_live_sync_enabled():
        import omni.kit.usd.layers as layers

        live_sync = layers.get_live_syncing()

        curr_session = live_sync.get_current_live_session()
        if curr_session:
            live_sync.stop_live_session()
            msg = "Successfully stopped live session."
            logger.info(msg)
            return MessageResponse(message=msg)
        else:
            msg = "User is not in a Live Session"
            logger.error(msg)
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=msg)
    else:
        msg = "Live Session option is not enabled, please enable it and verify if Live Menu is visible on top right corner of the app."
        logger.error(msg)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)


@router.get("/live_sessions/", tags=["Live Session"])
async def live_sessions():
    """
        Fetches all live sessions and returns them as a dictionary.

    This function fetches all live sessions and returns them as a dictionary. The keys of the dictionary are the names of the live sessions, and the values are their corresponding base layer identifiers.

    Returns:

        Dict[str, str]: A dictionary containing live session names as keys and their corresponding base layer identifiers as values.

    Raises:

        HTTPException: If no live sessions are found.
    """
    if is_live_sync_enabled():
        import omni.kit.usd.layers as layers

        session_list = {}
        live_sync = layers.get_live_syncing()

        sessions = live_sync.get_all_live_sessions()
        for session in sessions:
            session_list[session.name] = session.base_layer_identifier
        if session_list:
            msg = f"Fetched live sessions: {session_list}"
            logger.info(msg)
            return {"live_session_list": session_list}
        else:
            msg = "No live session exists for this stage."
            logger.error(msg)
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=msg)
    else:
        msg = "Live Session option is not enabled, please enable it and verify if Live Menu is visible on top right corner of the app."
        logger.error(msg)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)


@router.post(
    "/join_live_session/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Live Session"],
)
async def join_live_session(request: JoinSessionRequest):
    """
        Joins an existing live session with a given USD path and session name.

    This function joins an existing live session with a given USD path and session name.
    It returns a success message if the session is joined successfully. If no sessions with the given name or USD path are found, it raises an HTTPException with a 404 status code.

    Parameters:

        usd_path (str): The path to the USD file.
        session_name (str): The name of the session to join.

    Returns:

        MessageResponse: A response object containing the success message.

    Raises:

        HTTPException: If no sessions with the given name or USD path are found.
    """
    if is_live_sync_enabled():
        import omni.kit.usd.layers as layers

        live_sync = layers.get_live_syncing()
        all_sessions = live_sync.get_all_live_sessions()
        for session in all_sessions:
            if (
                session.base_layer_identifier == request.usd_path
                and session._session_name == request.session_name
            ):
                live_sync.join_live_session(session)
                msg = f"Successfully joined live session: {request.session_name} for USD {request.usd_path}"
                logger.info(msg)
                return MessageResponse(message=msg)
        msg = f"No sessions with name as {request.session_name} or for path as {request.usd_path} exists."
        logger.error(msg)
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=msg)
    else:
        msg = "Live Session option is not enabled, please enable it and verify if Live Menu is visible on top right corner of the app."
        logger.error(msg)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)


@router.post(
    "/create_live_session/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Live Session"],
)
async def create_live_session(request: CreateSessionRequest):
    """
        Creates a live session with an optional layer.

    This function creates a live session with an optional layer.
    It returns a success message if the session is created successfully. If the layer is not found or an internal server error occurs, it raises an HTTPException with a 500 status code.

    Parameters:

        session_name (str): The name of the session to create.
        layer_name (str, optional): The name of the layer to create. Defaults to None.

    Returns:

        MessageResponse: A response object containing the success message.

    Raises:

        HTTPException: If the layer is not found or an internal server error occurs.
    """
    if is_live_sync_enabled():
        import omni.kit.usd.layers as layers
        import omni.usd

        live_sync = layers.get_live_syncing()
        if request.layer_name:
            stage = omni.usd.get_context().get_stage()
            layer_list = stage.GetLayerStack()
            for layer in layer_list:
                if request.layer_name == layer.GetDisplayName():
                    layer_identifier = layer.identifier
                    session = live_sync.create_live_session(
                        request.session_name, layer_identifier
                    )
                    msg = f"Created live session {request.session_name} for layer {request.layer_name}"
                    logger.info(msg)
                    return MessageResponse(message=msg)
            msg = f"Layer with name {request.layer_name} not found."
            logger.error(msg)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
        else:
            session = live_sync.create_live_session(request.session_name)

        if session:
            msg = f"Session created with name {request.session_name}."
            logger.info(msg)
            return MessageResponse(message=msg)
        else:
            msg = f"Session was not created with name {request.session_name}."
            logger.error(msg)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)
    else:
        msg = "Live Session option is not enabled, please enable it and verify if Live Menu is visible on top right corner of the app."
        logger.error(msg)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)


@router.get(
    "/layer_identifier/",
    response_model=Dict[str, Union[str, Dict]],
    tags=["Live Session"],
)
def layer_identifier():
    """
        Fetches layer identifiers from the current USD stage and returns them as a dictionary.

    This function fetches layer identifiers from the current USD stage and returns them as a dictionary. The keys of the dictionary are the names of the layers, and the values are their corresponding identifiers.

    Returns:

        Dict[str, Union[str, Dict]]: A dictionary containing layer names as keys and their corresponding identifiers as values.
    """
    import omni.usd

    layers = {}
    stage = omni.usd.get_context().get_stage()
    layer_list = stage.GetLayerStack()

    for layer in layer_list:
        layers[layer.GetDisplayName()] = layer.identifier
        msg = f"Fetched layers: {layers}"
        logger.info(msg)

    return {"layer_identifiers": layers}
