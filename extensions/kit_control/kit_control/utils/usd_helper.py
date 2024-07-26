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
import html

logger = logging.getLogger("kit_control")


class UsdHelper:
    """
    A class with static methods for working with USD stages.

    This class provides several static methods for working with USD stages,
    such as getting the default camera path, getting the Xform of a prim,
    and setting the Xform of a prim.

    Methods:
        get_stage: Get the current USD stage.
        get_default_camera_path: Get the path to the default camera.
        getXform_from_current_stage: Get the Xform of a prim on the current stage.
        getXform: Get the Xform of a prim on a given stage.
        set_xform: Set the Xform of a prim on a given stage.
        add_and_set_test_camera: Add a test camera to the stage and set its Xform.
        get_visible_prims: Get a list of visible prims on the stage.
        get_invisible_prims: Get a list of invisible prims on the stage.
    """

    @staticmethod
    def get_stage():
        """
        Gets the current stage from USD context.

        Returns:
            The current stage from USD context.

        Raises:
            None.
        """
        import omni.usd as usd

        logger.info("Get stage from usd")
        return usd.get_context().get_stage()

    @staticmethod
    def get_default_camera_path():
        """
        Gets the default camera path.

        Returns:
            The default camera path string.

        Raises:
            None.
        """
        from omni.kit.viewport.utility import get_active_viewport_camera_string

        logger.info("Get default camera path")
        return get_active_viewport_camera_string()

    @staticmethod
    def getXform_from_current_stage(prim_path: str, time=0):
        """
        Retrieves the Xform vectors from the current stage.

        Parameters:
            prim_path: The prim path as a string.
            time: The time at which to retrieve the Xform vectors. Default is 0.

        Returns:
            The Xform vectors of the prim at the given path and time.

        Raises:
            RuntimeError: If the prim is invalid or does not exist.
        """
        from pxr import UsdGeom

        prim_path_escaped = html.escape(prim_path)
        stage = UsdHelper.get_stage()
        prim = stage.GetPrimAtPath(prim_path)
        try:
            xform = UsdGeom.XformCommonAPI(prim).GetXformVectors(time)
        except RuntimeError:
            logger.error(
                "Prim invalid/Prim does not exist for path %s", prim_path_escaped
            )
            raise

        logger.info(f"Xform of prim at path{prim_path_escaped} -> {xform}")
        return xform

    @staticmethod
    def getXform(stage, prim_path: str, time=0):
        """
        Gets the xform of a given prim path.

        Parameters:
            prim_path (str): The path of the prim.
            time (int, optional): The time at which to get the xform. Defaults to 0.

        Returns:
            The xform of the prim at the given path and time.

        Raises:
            RuntimeError: If the prim is invalid or does not exist.
        """
        from pxr import UsdGeom

        logger.info("Get xform of given prim path")
        prim = stage.GetPrimAtPath(prim_path)
        try:
            xform = UsdGeom.XformCommonAPI(prim).GetXformVectors(time)
        except RuntimeError:
            logger.info(f"Prim invalid/Prim does not exist: {prim_path}")
            raise
        logger.info(f"Xform of prim at path '{prim_path}' -> {xform}")

        return xform

    @staticmethod
    def set_xform(stage, prim_path: str, xform: tuple):
        """
        Sets the given transform to the prim path.

        Parameters:
            stage: The stage object.
            prim_path (str): The prim path.
            xform (tuple): The transform tuple.

        Raises:
            RuntimeError: If the prim is invalid or does not exist.
        """
        from pxr import UsdGeom

        logger.info("Set given xform to prim path")
        prim = stage.GetPrimAtPath(prim_path)
        rotation_order_dict = {
            UsdGeom.XformCommonAPI.RotationOrderYXZ: "rotateYXZ",
            UsdGeom.XformCommonAPI.RotationOrderXYZ: "rotateXYZ",
            UsdGeom.XformCommonAPI.RotationOrderXZY: "rotateXZY",
            UsdGeom.XformCommonAPI.RotationOrderYZX: "rotateYZX",
            UsdGeom.XformCommonAPI.RotationOrderZXY: "rotateZXY",
            UsdGeom.XformCommonAPI.RotationOrderZYX: "rotateZYX",
        }

        try:
            UsdGeom.XformCommonAPI(prim).SetTranslate(translation=xform[0])
            UsdGeom.XformCommonAPI(prim).SetPivot(pivot=xform[3])

            if "test_camera" in prim_path:
                UsdGeom.XformCommonAPI(prim).SetRotate(
                    rotation=xform[1], rotationOrder=xform[4]
                )
                UsdGeom.XformCommonAPI(prim).SetScale(scale=xform[2])
            else:
                rotate_att = prim.GetAttribute(
                    "xformOp:" + rotation_order_dict[xform[4]]
                )
                rotate_att.Set(xform[1])
                scale_att = prim.GetAttribute("xformOp:scale")
                scale_att.Set(xform[2])
        except RuntimeError:
            logger.info(f"Prim invalid/Prim does not exist: {prim_path}")
            raise

    @staticmethod
    def add_and_set_test_camera(stage, camera_name="test_camera", xform=None):
        """
        Adds and sets a test camera in the stage.

        Parameters:
            stage: The stage to add the camera to.
            camera_name: The name of the camera. Default is 'test_camera'.
            xform: The transformation matrix for the camera. Default is None.

        This function imports necessary modules, gets the active stage, and creates a new camera with the given name.
        It sets the focal length of the camera and applies the given transformation matrix.
        Finally, it sets the active viewport to the newly created camera.
        """
        import omni.kit.commands
        import omni.usd
        from omni.kit.viewport.menubar.camera.commands import SetViewportCameraCommand
        from omni.kit.viewport.utility import get_active_viewport
        from pxr import Sdf

        stage = UsdHelper.get_stage()
        if not xform:
            xform = UsdHelper.getXform(stage, UsdHelper.get_default_camera_path())

        viewport_api = get_active_viewport()
        target_path = omni.usd.get_stage_next_free_path(stage, "/" + camera_name, True)
        omni.kit.commands.execute(
            "CreatePrimWithDefaultXformCommand",
            prim_path=target_path,
            prim_type="Camera",
            create_default_xform=False,
        )

        omni.kit.commands.execute(
            "ChangeProperty",
            prop_path=Sdf.Path(f"/World/{camera_name}.focalLength"),
            value=18.14756,
            prev=50.0,
        )

        UsdHelper.set_xform(stage, target_path, xform)
        SetViewportCameraCommand(target_path, viewport_api).do()

    @staticmethod
    def get_visible_prims(stage):
        """
        Gets the paths of visible prims in the stage.

        Parameters:
            stage: The stage to traverse.

        Returns:
            A list of strings representing the paths of visible prims.

        Raises:
            No exceptions are raised by this method.
        """
        from pxr import UsdGeom

        invisible_assets = []

        for prim in stage.Traverse():
            if UsdGeom.Imageable(prim).ComputeVisibility() != UsdGeom.Tokens.invisible:
                invisible_assets.append(str(prim.GetPath()))

        return invisible_assets

    @staticmethod
    def get_invisible_prims(stage):
        """
        Gets a list of invisible prims in the given stage.

        Parameters:
            stage: The stage to traverse and find invisible prims.

        Returns:
            A list of strings representing the paths of the invisible prims.

        Raises:
            None.
        """
        from pxr import UsdGeom

        invisible_assets = []

        for prim in stage.Traverse():
            if UsdGeom.Imageable(prim).ComputeVisibility() == UsdGeom.Tokens.invisible:
                invisible_assets.append(str(prim.GetPath()))

        return invisible_assets
