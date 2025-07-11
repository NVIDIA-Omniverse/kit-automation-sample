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

logger = logging.getLogger("omni.kit.test.automation.sample")


def logging_init(level):
    """
    Initialize logging for the automation sample module.

    Args:
        level (int): The logging level to use.
    """
    import sys

    path = get_log_path()
    file_handler = logging.FileHandler(f"{path}", "a")
    file_handler.setLevel(logging.INFO)
    file_handler.name = "file_handler"
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.name = "console_handler"

    logger = logging.getLogger("omni.kit.test.automation.sample")
    logger.propagate = False
    
    
    if len(logger.handlers) == 0:
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(name)s] [%(levelname)s] [%(filename)s] [%(funcName)s %(lineno)s] - %(message)s"
            )
        )
        logger.addHandler(file_handler)
        console_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(name)s] [%(levelname)s] [%(filename)s] [%(funcName)s %(lineno)s] - %(message)s"
            )
        )
        logger.addHandler(console_handler)
    logger.info(f"Logging initialized for omni.kit.test.automation.sample at {path}")


def get_log_path() -> str:
    """
    Get the path to the log file for the automation sample module.

    Returns:
        str: The path to the log file.
    """
    from datetime import datetime

    import carb.tokens

    path = (
        carb.tokens.get_tokens_interface().resolve("${omni_logs}") + "/Kit/automation_sample"
    )

    if os.path.exists(path):
        return (
            path
            + f"/automation_sample_{datetime.now().hour}{datetime.now().minute}{datetime.now().second}.log"
        )
    else:
        os.mkdir(path)
        return (
            path
            + f"/automation_sample_{datetime.now().hour}{datetime.now().minute}{datetime.now().second}.log"
        )
