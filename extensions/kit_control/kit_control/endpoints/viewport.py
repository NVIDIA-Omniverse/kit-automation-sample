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
from typing import Any, Dict, Union

import omni.kit.ui_test as ui_test
from omni.kit.ui_test.query import WidgetRef
from omni.kit.ui_test.vec2 import Vec2
from omni.services.core import routers

logger = logging.getLogger("kit_control")
from fastapi import HTTPException, status

router = routers.ServiceAPIRouter()
from ..api_models.common_models import MessageResponse
from ..api_models.viewport_models import (
    CameraSettingsResponse,
    CoordinateViewportRequest,
    ViewportScreenshotRequest,
    ViewportScreenshotResponse,
    ZoomViewportRequest,
)

camera_initial_state = {}


@router.post(
    "/capture_viewport_screenshot/",
    response_model=ViewportScreenshotResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Viewport"],
)
async def capture_viewport_screenshot(request: ViewportScreenshotRequest):
    """
        Capture a viewport screenshot.

    This function captures a screenshot of the active viewport and saves it to a specified directory.

    Valid formats - `png` and `jpeg`

    Path examples - `C:/users/user/screenshot.png`

    Parameters:

        request (ViewportScreenshotRequest): The request object containing the screenshot parameters.
            - dir (str): The file path to save the screenshot to along with the file name and format.

    Returns:

        Union[FileResponse, ViewportScreenshotResponse]: A response object containing the file path and
            message if the screenshot was saved to the server, or a file response object if the
            screenshot was downloaded.

    Raises:

        HTTPException: An error occurred while capturing the screenshot.

    """
    from omni.kit.viewport.utility import capture_viewport_to_file, get_active_viewport

    viewport = get_active_viewport()

    if "jpeg" in request.dir or "png" in request.dir:
        try:
            capture_viewport_to_file(viewport_api=viewport, file_path=request.dir)
            logger.info("Viewport screenshot captured successfully.")
            return ViewportScreenshotResponse(
                file_path=request.dir,
                message="Viewport screenshot captured successfully.",
            )

        except Exception as e:
            msg = f"Error capturing viewport screenshot: {str(e)}"
            logger.error(msg)
            raise HTTPException(status_code=500, detail=msg)

    else:
        msg = f"Error capturing viewport screenshot: Please specify the format png or jpeg"
        raise HTTPException(status_code=500, detail=msg)


@router.post(
    "/zoom_viewport/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Viewport"],
)
async def zoom_viewport(request: ZoomViewportRequest):
    """
        Zoom viewport API

    X and Y values are coordinates values calculated from center of the Viewport window. The mouse if moved to the specified coordinate while performing the action.

    Example values:

        x: 100 y:500

    Parameters:

        request (ZoomViewportRequest): Request object containing direction, x, and y.
            - direction (str): The direction of the zoom. Can be 'IN' or 'OUT'.
            - x (float): The x-coordinate of the point to zoom in/out around.
            - y (float): The y-coordinate of the point to zoom in/out around.

    Returns:

        MessageResponse: A response object containing a success message indicating the result of the zoom operation.

    Raises:

        HTTPException: An error occurred while zooming the viewport.
    """
    from ..utils.usd_helper import UsdHelper

    try:
        global camera_initial_state
        stage = UsdHelper.get_stage()
        camera_path = UsdHelper.get_default_camera_path()
        if "/OmniverseKit_Persp" in camera_path:
            xform = UsdHelper.getXform(stage, camera_path)
            UsdHelper.add_and_set_test_camera(stage, xform=xform)
            camera_path = UsdHelper.get_default_camera_path()
        if (stage, camera_path) not in camera_initial_state:
            camera_initial_state[(stage, camera_path)] = UsdHelper.getXform(
                stage, camera_path
            )
        viewport = ui_test.find("Viewport//Frame/ZStack[0]/ZStack[0]/Frame[0]")
        await ui_test.emulate_mouse_move(viewport.center)
        logger.info(f"Start position: {viewport.center}")
        (
            await ui_test.emulate_mouse_scroll(Vec2(request.x, request.y))
            if request.direction.lower() == "in"
            else await ui_test.emulate_mouse_scroll(Vec2(-request.x, -request.y))
        )
        msg = f"Viewport zoomed in direction {request.direction} with values {request.x,request.y}"
        logger.info(msg)
        return MessageResponse(message=msg)
    except Exception as e:
        msg = f"Error performing zoom viewport: {str(e)}"
        logger.error(msg)
        raise HTTPException(status_code=500, detail=msg)


@router.post(
    "/rotate_viewport/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Viewport"],
)
async def rotate_viewport(request: CoordinateViewportRequest):
    """
        Rotate the viewport by clicking at viewport center and then dragging the mouse to user specified coordinates

    X and Y values are coordinates values calculated from center of the Viewport window. The mouse if moved to the specified coordinate while performing the action.

    Example values:

        x: 100 y:500
        x: 100 y:-500

    Parameters:

        request (CoordinateViewportRequest): Request object containing x and y.
            - x (float): The x-coordinate to move the viewport to.
            - y (float): The y-coordinate to move the viewport to.

    Returns:

        MessageResponse: A response object containing a success message indicating the result of the rotation operation.

    Raises:

        HTTPException: An error occurred while rotating the viewport.
    """
    import carb
    from carb.input import KeyboardEventType, KeyboardInput, MouseEventType

    from ..utils.usd_helper import UsdHelper

    global camera_initial_state
    stage = UsdHelper.get_stage()
    camera_path = UsdHelper.get_default_camera_path()
    if "/OmniverseKit_Persp" in camera_path:
        xform = UsdHelper.getXform(stage, camera_path)
        UsdHelper.add_and_set_test_camera(stage, xform=xform)
        camera_path = UsdHelper.get_default_camera_path()
    if (stage, camera_path) not in camera_initial_state:
        camera_initial_state[(stage, camera_path)] = UsdHelper.getXform(
            stage, camera_path
        )

    try:
        viewport_widget: WidgetRef = ui_test.find(
            "Viewport//Frame/ZStack[0]/ZStack[0]/Rectangle[0]"
        )
        center: Vec2 = viewport_widget.center

        x = center.x + request.x
        y = center.y - request.y

        if x < 0:
            x = 0
        elif x > viewport_widget.size.x:
            x = viewport_widget.size.x
        if y < 0:
            y = 0
        elif y > viewport_widget.size.y:
            y = viewport_widget.size.y

        await ui_test.input.emulate_mouse(MouseEventType.MOVE, center)
        await ui_test.input.emulate_keyboard(
            KeyboardEventType.KEY_PRESS,
            KeyboardInput.LEFT_ALT,
            carb.input.KEYBOARD_MODIFIER_FLAG_ALT,
        )
        await ui_test.input.emulate_mouse(MouseEventType.LEFT_BUTTON_DOWN)
        await ui_test.input.human_delay(20)
        await ui_test.input.emulate_mouse_slow_move(
            center, Vec2(x, y), human_delay_speed=20
        )
        await ui_test.input.human_delay(20)
        await ui_test.input.emulate_mouse(MouseEventType.LEFT_BUTTON_UP)
        await ui_test.input.emulate_keyboard(
            KeyboardEventType.KEY_RELEASE,
            KeyboardInput.LEFT_ALT,
            carb.input.KEYBOARD_MODIFIER_FLAG_ALT,
        )
        msg = f"Viewport rotated with values {request.x,request.y}"
        logger.info(msg)
        return MessageResponse(message=msg)
    except Exception as e:
        msg = f"Error performing rotate viewport: {str(e)}"
        logger.error(msg)
        raise HTTPException(status_code=500, detail=msg)


@router.post(
    "/pan_viewport/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Viewport"],
)
async def pan_viewport(request: CoordinateViewportRequest):
    """
        Pan the viewport by clicking at viewport center and then dragging the mouse to user specified coordinates

    X and Y values are coordinates values calculated from center of the Viewport window. The mouse if moved to the specified coordinate while performing the action.

    Example values:

        x: 100 y:500
        x: 100 y:-500

    Parameters:

        request (CoordinateViewportRequest): Request object containing x and y.
            - x (float): The x-coordinate to move the viewport to.
            - y (float): The y-coordinate to move the viewport to.

    Returns:

        MessageResponse: A response object containing a success message indicating the result of the pan operation.

    Raises:

        HTTPException: An error occurred while panning the viewport.
    """
    from carb.input import MouseEventType

    from ..utils.usd_helper import UsdHelper

    global camera_initial_state
    stage = UsdHelper.get_stage()
    camera_path = UsdHelper.get_default_camera_path()
    if "/OmniverseKit_Persp" in camera_path:
        xform = UsdHelper.getXform(stage, camera_path)
        UsdHelper.add_and_set_test_camera(stage, xform=xform)
        camera_path = UsdHelper.get_default_camera_path()
    if (stage, camera_path) not in camera_initial_state:
        camera_initial_state[(stage, camera_path)] = UsdHelper.getXform(
            stage, camera_path
        )

    try:
        viewport_widget: WidgetRef = ui_test.find(
            "Viewport//Frame/ZStack[0]/ZStack[0]/Rectangle[0]"
        )
        center: Vec2 = viewport_widget.center

        x = center.x + request.x
        y = center.y - request.y

        if x < 0:
            x = 0
        elif x > viewport_widget.size.x:
            x = viewport_widget.size.x
        if y < 0:
            y = 0
        elif y > viewport_widget.size.y:
            y = viewport_widget.size.y

        await ui_test.input.emulate_mouse(MouseEventType.MOVE, center)
        await ui_test.input.emulate_mouse(MouseEventType.MIDDLE_BUTTON_DOWN)
        await ui_test.input.human_delay(20)
        await ui_test.input.emulate_mouse_slow_move(
            center, Vec2(x, y), human_delay_speed=20
        )
        await ui_test.input.human_delay(20)
        await ui_test.input.emulate_mouse(MouseEventType.MIDDLE_BUTTON_UP)
        msg = f"Viewport panned with values {request.x,request.y}"
        logger.info(msg)
        return MessageResponse(message=msg)
    except Exception as e:
        msg = f"Error performing pan viewport: {str(e)}"
        logger.error(msg)
        raise HTTPException(status_code=500, detail=msg)


@router.post(
    "/reset_default_camera/", status_code=status.HTTP_201_CREATED, tags=["Viewport"]
)
async def reset_default_camera() -> dict:
    """
        Reset the default camera to its initial state.

    If the initial state is not available, store the current state as the initial state.

    Returns:

        dict: A dictionary containing the message.
    """
    from ..utils.usd_helper import UsdHelper

    global camera_initial_state

    stage = UsdHelper.get_stage()
    camera_path = UsdHelper.get_default_camera_path()
    if (stage, camera_path) in camera_initial_state:
        UsdHelper.set_xform(
            stage,
            camera_path,
            camera_initial_state[(stage, camera_path)],
        )
        logger.info("Camera reset successful")
        return {
            "message": "Initial camera state found and restored.",
        }
    else:
        logger.info(
            "Initial camera state not available. Stored current state as initial state."
        )
        if "/OmniverseKit_Persp" in camera_path:
            xform = UsdHelper.getXform(stage, camera_path)
            UsdHelper.add_and_set_test_camera(stage, xform=xform)
            camera_path = UsdHelper.get_default_camera_path()
        camera_initial_state[(stage, camera_path)] = UsdHelper.getXform(
            stage, camera_path
        )
        return {
            "message": "Initial camera state not found. Stored current state as initial state.",
        }


@router.get(
    "/viewport_info/", response_model=Dict[str, Dict[str, Any]], tags=["Viewport"]
)
async def viewport_info():
    """
        Gets viewport frame information like render mode, frametime, vram info and metadata.

    Returns:

        Dict[str, Dict[str, Any]]: A dictionary containing the viewport frame information.
    """
    from omni.hydra.engine.stats import get_device_info
    from omni.kit.viewport.utility import get_active_viewport

    frame_info = {}
    try:
        viewport = get_active_viewport()
        if viewport:
            frame_info = viewport.frame_info
            frame_info["render_mode"] = viewport.render_mode
            frame_info["frame_time"] = (
                round(1000 / viewport.fps, 2) if viewport.fps else 9999
            )
            frame_info["vram_info"] = get_device_info()
            if frame_info.get("metadata", None):
                frame_info.pop("metadata")
            msg = f"Viewport information captured {frame_info}"
            logging.info(msg)
            return {"viewport_info": frame_info}
    except Exception as e:
        msg = f"Viewport information capture failed: {str(e)}"
        logging.error(msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg
        )


@router.put(
    "/set_viewport_resolution/",
    response_model=Union[MessageResponse],
    status_code=status.HTTP_201_CREATED,
    tags=["Viewport"],
)
async def viewport_resolution(res: str):
    """
        Sets the viewport resolution.

    Supported resolutions are: {"HD": (1280, 720), "FHD": (1920, 1080), "4K": (3840, 2160)}
    Custom resolutions can also be set by passing the width and height separated by an `X`, e.g. `1280X720`.

    If any of the supported resolution is being sent then either the key or the resolution value separated by X can be sent.

    Example inputs:

        1. HD
        2. 1280x720
        3. 900x600

    Parameters:

        res (str): The resolution to set.

    Returns:

        MessageResponse: A response object containing a success message indicating the result of the resolution setting operation.

    Raises:

        HTTPException: An error occurred while setting the viewport resolution.
    """
    import carb.settings
    from omni.kit.viewport.utility import get_active_viewport

    RESOLUTIONS = {"HD": (1280, 720), "FHD": (1920, 1080), "4K": (3840, 2160)}

    viewport = get_active_viewport()

    if viewport:
        res = res.upper()
        if res in RESOLUTIONS:
            resolution = RESOLUTIONS[res]
        elif "X" in res:
            try:
                width, height = map(int, res.split("X"))
                resolution = (width, height)
            except ValueError:
                msg = f"Received incorrect resolution format: {res}"
                logger.error(msg)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, message=msg
                )
        else:
            msg = f"Received incorrect resolution format: {res}"
            logger.error(msg)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

        viewport.fill_frame = False
        settings = carb.settings.get_settings()
        settings.set(f"/persistent/app/viewport/{viewport.id}/fillViewport", False)

        viewport.resolution = resolution
        message = f"Viewport resolution successfully set: {resolution}"
        logger.info(message)
        return MessageResponse(message=message)
    else:
        msg = "Could not find active viewport"
        logger.error(msg)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)


@router.post(
    "/fill_viewport/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Viewport"],
)
async def fill_viewport():
    """
        Fill the viewport.

    Set the viewport to fill the frame.

    Returns:

        MessageResponse: A response object containing a success message indicating the result of the fill viewport operation.

    Raises:

        HTTPException: An error occurred while filling the viewport.
    """
    from omni.kit.viewport.utility import get_active_viewport

    viewport = get_active_viewport()

    if viewport:
        viewport.fill_frame = True
        msg = f"Viewport successfully filled"
        logger.info(msg)
        return MessageResponse(message=msg)
    else:
        msg = "Could not find active viewport"
        logger.error(msg)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)


@router.get("/lighting_mode", response_model=Dict[str, str], tags=["Viewport"])
async def lighting_mode():
    """
        Get the current lighting mode for the active viewport.

    Returns:

        Dict[str, str]: A dictionary containing the lighting mode.

    Raises:

        HTTPException: If the active viewport or USD context cannot be found.
    """
    import carb.settings
    from omni.kit.viewport.utility import get_active_viewport
    from pxr import UsdUtils

    viewport = get_active_viewport()
    settings = carb.settings.get_settings()
    if viewport:
        usd_context = viewport.usd_context
        if usd_context:
            stage = usd_context.get_stage()
            if stage:
                stage_id = UsdUtils.StageCache.Get().GetId(stage).ToLongInt()
                lighting_mode = settings.get(
                    f"/exts/omni.kit.viewport.menubar.lighting/lightingMode/{stage_id}"
                )
                if not lighting_mode:
                    lighting_mode = "stage"
                message = f"Fetched lighting mode: {lighting_mode}"
                logger.info(message)
                return {"lighting_mode": lighting_mode}
            else:
                msg = "Could not fetch stage from the USD Context"
                logger.error(msg)
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
        else:
            msg = "Could not USD Context"
            logger.error(msg)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
    else:
        msg = "Could not find active viewport"
        logger.error(msg)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)


@router.post(
    "/toggle_renderer/",
    status_code=status.HTTP_201_CREATED,
    response_model=MessageResponse,
    tags=["Viewport"],
)
async def toggle_renderer(renderer: str):
    """
    This API will toggle the renderer between Realtime, Iray, PathTracing and Pixar using non UI route.

    `Note`:

        This API will not switch renderer if current active renderer is same.

    Valid renderer values are: 'realtime', 'pathtracing', 'iray', 'pixar'.

    Parameters:

        renderer (str): The renderer to toggle to.

    Returns:

        MessageResponse: A response object containing a success message indicating the result of the renderer toggle operation.

    Raises:

        HTTPException: An error occurred while toggling the renderer.
    """
    renderers = {
        "realtime": "RaytracedLighting",
        "pathtracing": "PathTracing",
        "iray": "iray",
        "pixar": "pxr",
    }

    if renderer.lower() in renderers.keys():
        from omni.kit.viewport.utility import get_active_viewport

        active_viewport = get_active_viewport()
        logger.info(f"Changing the active renderer to : {renderer}")

        if renderer.lower() in ["realtime", "pathtracing"]:
            active_viewport.set_hd_engine("rtx", renderers[renderer.lower()])

        elif renderer.lower() == "iray":
            active_viewport.set_hd_engine("iray", "iray")
        else:
            active_viewport.set_hd_engine(renderers[renderer.lower()])

        message = f"Set viewport renderer as: {renderer}"
        logger.info(message)
        return MessageResponse(message=message)
    else:
        msg = f"Invalid renderer received, valid options are {renderers.keys()}"
        logger.error(msg)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)


@router.get(
    "/camera_details/", response_model=CameraSettingsResponse, tags=["Viewport"]
)
async def camera_details():
    """
        This endpoint fetches the current camera settings using stage context.

    Returns:

        CameraSettingsResponse: A response object containing the following attributes:
            - camera_path (str): The path to the camera.
            - speed (dict, optional): The camera speed settings.
            - exposure (dict, optional): The camera exposure settings.
            - lens (dict, optional): The camera lens settings.

    Raises:

        HTTPException: An error occurred while fetching the camera settings.
    """
    import carb.settings

    from ..utils.usd_helper import UsdHelper

    settings = carb.settings.get_settings()

    camera_speed = settings.get("/persistent/app/viewport/camMoveVelocity")
    camera_speed_min = settings.get("/persistent/app/viewport/camVelocityMin")
    camera_speed_max = settings.get("/persistent/app/viewport/camVelocityMax")

    auto_exposure = bool(settings.get("/rtx/post/histogram/enabled"))
    camera_exposure_value = settings.get("/rtx/post/histogram/whiteScale")
    camera_iso_value = settings.get("/rtx/post/tonelement_cache/filmIso")

    stage = UsdHelper.get_stage()
    camera_path = UsdHelper.get_default_camera_path()

    speed = {
        "current_speed": camera_speed,
        "camera_speed_min": camera_speed_min,
        "camera_speed_max": camera_speed_max,
    }
    exposure = {
        "auto_exposure_enabled": auto_exposure,
        "camera_exposure_value": camera_exposure_value,
        "camera_iso_value": camera_iso_value,
    }
    if stage and camera_path:
        camera_focal_length = stage.GetPropertyAtPath(
            f"{camera_path}.focalLength"
        ).Get()
        camera_focus_distance = stage.GetPropertyAtPath(
            f"{camera_path}.focusDistance"
        ).Get()
        camera_f_stop_value = stage.GetPropertyAtPath(f"{camera_path}.fStop").Get()

        lens = {
            "camera_focal_length": camera_focal_length,
            "camera_focus_distance": camera_focus_distance,
            "camera_f_stop_value": camera_f_stop_value,
        }
        return CameraSettingsResponse(
            camera_path=camera_path, speed=speed, exposure=exposure, lens=lens
        )
    else:
        msg = "Failed to fetch stage context or camera_path"
        logger.error(msg)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)