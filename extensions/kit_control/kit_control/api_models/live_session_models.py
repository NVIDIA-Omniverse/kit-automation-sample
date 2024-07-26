# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.


from typing import Optional

from pydantic import BaseModel


class JoinSessionRequest(BaseModel):
    """
    Model representing a request to join a USD session.

    Attributes:
    
        usd_path (str): The path to the USD file.
        session_name (str): The name of the session to join.
    """

    usd_path: str
    session_name: str


class CreateSessionRequest(BaseModel):
    """
    Model representing a request to create a USD session.

    Attributes:
    
        session_name (str): The name of the session to create.
        layer_name (str, optional): The name of the layer to create. Defaults to
            None.
    """

    session_name: str
    layer_name: Optional[str] = None
