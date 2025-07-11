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

import carb
import carb.settings
import omni.ext
from omni.services.core import main

from .endpoints.coverage import router as coverage_router
from .endpoints.extension import router as extension_router
from .endpoints.keyboard import router as keyboard_router
from .endpoints.live_session import router as live_session
from .endpoints.menu import router as menu_router
from .endpoints.misc import router as misc
from .endpoints.mouse import router as mouse_router
from .endpoints.nucleus import router as nucleus_router
from .endpoints.query import router as query_router
from .endpoints.usd import router as usd_router
from .endpoints.viewport import router as viewport_router
from .endpoints.widget import router as widget_router
from .endpoints.window import router as window_router
from .utils.logging import logging_init


class AutomationSampleExtension(omni.ext.IExt):

    def __init__(self) -> None:
        """
        Initializes the class.

        This method initializes the class and sets up logging.

        Args:
        None

        Returns:
        None

        Raises:
        None"""
        super().__init__()
        self._settings = carb.settings.get_settings()

        log_level = self._settings.get("exts/omni.kit.test.automation.sample/log_level") or logging.INFO
        logging_init(log_level)
        self.logger = logging.getLogger("omni.kit.test.automation.sample")

    def on_startup(self):
        """
        Registers all necessary routers for the automation sample extension.

        This function is called on startup and registers various routers such as query_router, mouse_router, keyboard_router, menu_router, window_router, widget_router, extension_router, viewport_router, coverage_router, usd_router, nucleus_router, live_session, and misc.

        Args:
            self: The instance of the class.

        Raises:
            None."""
        main.register_router(router=query_router)
        main.register_router(router=mouse_router)
        main.register_router(router=keyboard_router)
        main.register_router(router=menu_router)
        main.register_router(router=window_router)
        main.register_router(router=widget_router)
        main.register_router(router=extension_router)
        main.register_router(router=viewport_router)
        main.register_router(router=coverage_router)
        main.register_router(router=usd_router)
        main.register_router(router=nucleus_router)
        main.register_router(router=live_session)
        main.register_router(router=misc)
        self.logger.info(
            "Successfully registered omni.kit.test.automation.sample extension router in to omni.services.core main router."
        )

    def on_shutdown(self):
        """
        Deregisters all routers and logs a successful de-registration message.

        This function deregisters the following routers:
        - keyboard_router
        - menu_router
        - mouse_router
        - query_router
        - viewport_router
        - nucleus_router
        - usd_router
        - coverage_router
        - window_router
        - widget_router
        - extension_router
        - live_session
        - misc

        After deregistering all routers, it logs a successful de-registration message.

        Raises:
        Any exceptions raised by the deregister_router method."""
        main.deregister_router(router=keyboard_router)
        main.deregister_router(router=menu_router)
        main.deregister_router(router=mouse_router)
        main.deregister_router(router=query_router)
        main.deregister_router(router=viewport_router)
        main.deregister_router(router=nucleus_router)
        main.deregister_router(router=usd_router)
        main.deregister_router(router=coverage_router)
        main.deregister_router(router=window_router)
        main.deregister_router(router=widget_router)
        main.deregister_router(router=extension_router)
        main.deregister_router(router=live_session)
        main.deregister_router(router=misc)
        self.logger.info(
            "Successfully de-registered omni.kit.test.automation.sample extension router from omni.services.core main router."
        )
