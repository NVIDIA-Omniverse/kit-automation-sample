# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.


from typing import Dict, List

from pydantic import BaseModel


class PrimTransformPropertiesResponse(BaseModel):
    """
    Model representing a response for getting a prim's transform properties.

    Attributes:
    
        prim_path (str): The path to the prim.
        translate (Dict[str, float]): The translate properties of the prim.
        rotate (Dict[str, float]): The rotate properties of the prim.
        scale (Dict[str, float]): The scale properties of the prim.
    """

    prim_path: str
    translate: Dict[str, float]
    rotate: Dict[str, float]
    scale: Dict[str, float]
