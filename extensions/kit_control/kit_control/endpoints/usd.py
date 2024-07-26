# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.


import html
import logging
from typing import Any, Dict, List

from fastapi import HTTPException, status
from omni.kit.viewport.utility import get_active_viewport_window
from omni.services.core import routers

from ..api_models.usd_models import PrimTransformPropertiesResponse
from ..utils.usd_helper import UsdHelper

logger = logging.getLogger("kit_control")

router = routers.ServiceAPIRouter()


@router.get(
    "/prim_transform_properties/",
    response_model=PrimTransformPropertiesResponse,
    tags=["USD API"],
)
async def prim_transform_properties(prim_path: str):
    """
        Fetch transform properties of multiple primes in the stage.

    This endpoint fetches the transform properties of multiple prims in the stage using their paths and returns the properties.
    If the prims already have their transform properties cached, the cached values are returned directly.

    Parameters:
    
        prim_path (str): The paths of the prime to fetch the transform properties for.

    Returns:
    
        PrimTransformPropertiesResponse: A response object containing the transform properties of the found primes.

    Raises:
    
        HTTPException: If the request is invalid or no primes could be found.
    """
    try:
        prim_path = html.escape(prim_path)
        xform = UsdHelper.getXform_from_current_stage(prim_path=prim_path)
        translate = {
            "x": xform[0][0],
            "y": xform[0][1],
            "z": xform[0][2],
        }
        rotate = {
            "x": xform[1][0],
            "y": xform[1][1],
            "z": xform[1][2],
        }
        scale = {
            "x": xform[2][0],
            "y": xform[2][1],
            "z": xform[2][2],
        }
        pivot = {
            "x": xform[3][0],
            "y": xform[3][1],
            "z": xform[3][2],
        }
        logger.info(
            f"Fetched coordinates of prim at path {prim_path}: \nTranslate: {translate}, Rotate: {rotate}, Scale:"
            f" {scale}, Pivot: {pivot}"
        )
        return PrimTransformPropertiesResponse(
            prim_path=prim_path,
            translate=translate,
            rotate=rotate,
            scale=scale,
            pivot=pivot,
        )
    except Exception as e:
        msg = f"Prim invalid/Prim does not exist using {prim_path} Error:{str(e)}"
        logger.error(msg)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)


@router.get(
    "/prim_screen_coordinate/",
    response_model=Dict[str, Dict[str, float]],
    tags=["USD API"],
)
def get_prim_screen_coordinate(prim_path: str) -> Dict[str, Dict[str, float]]:
    """
        Get the screen coordinate of a prim in the active viewport window.

    Parameters:
    
        prim_path (str): The prim path.

    Returns:
    
        Dict[str, Dict[str, float]]: A dictionary containing the screen coordinate of the prim.

    Raises:
    
        HTTPException: If there's an error while fetching the screen coordinate.
    """
    stage = UsdHelper.get_stage()

    try:
        window = get_active_viewport_window()
        if window is None:
            raise RuntimeError("No active viewport window found.")

        api = window.viewport_api

        prim = stage.GetPrimAtPath(prim_path)
        if prim.GetAttribute("xformOp:translate").Get() is None:
            raise RuntimeError("Prim does not have a valid position.")

        position = prim.GetAttribute("xformOp:translate").Get()
        # Convert NDC to Screen Space
        ndc_coord = api.world_to_ndc.Transform(position)

        screen_x = (ndc_coord[0] + 1) * 0.5
        screen_y = 1.0 - ((ndc_coord[1] + 1) * 0.5)

        # Apply Window Size
        mouse_x = screen_x * window.width
        mouse_y = screen_y * window.height

        return {"screen_coordinate": {"x": mouse_x, "y": mouse_y}}
    except RuntimeError as exc:
        msg = f"Failed to get screen coordinate for prim {prim_path}: {exc}"
        logger.error(msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg
        )


@router.get("/prims_visibility/", response_model=Dict[str, List[str]], tags=["USD API"])
async def get_prims_visibility() -> Dict[str, List[str]]:
    """
        Fetches list of visible and invisible prims in the scene.

    Returns:
    
        Dict[str, List[str]]: A dictionary containing the list of visible and invisible prims.

    Raises:
    
        HTTPException: If there's an error while fetching the prims visibility.
    """
    try:
        stage = UsdHelper.get_stage()
        visible = UsdHelper.get_visible_prims(stage)
        invisible = UsdHelper.get_invisible_prims(stage)
        logger.info("Fetched list of visible and invisible prims.")
        return {"visible_prims": visible, "invisible_prims": invisible}
    except RuntimeError as exc:
        msg = f"Failed to get visible and invisible prims: {exc}"
        logger.error(msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg
        )


@router.get(
    "/prim_material_mapping/",
    response_model=Dict[str, Dict[str, List[str]]],
    tags=["USD API"],
)
async def get_prim_material_mapping() -> Dict[str, Dict[str, List[str]]]:
    """
        Fetches mapping of prims with their materials.

    Returns:
    
        Dict[str, Dict[str, List[str]]]: A dictionary containing the mapping of prims and their materials.

    Raises:
    
        HTTPException: If there's an error while fetching the prim-material mapping.
    """
    try:
        stage = UsdHelper.get_stage()
        mapping = {}
        for prim in stage.Traverse():
            relationship = prim.GetRelationship("material:binding")
            materials = relationship.GetTargets()
            if len(materials) > 0:
                mapping[prim.GetPath().pathString] = [
                    material.pathString for material in materials
                ]
        logger.info("Fetched mapping of prims and materials.")
        return {"mapping": mapping}
    except Exception as exc:
        msg = f"Failed to get prim-material mapping: {exc}"
        logger.error(msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg
        )
