# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.


from typing import Dict, List, Optional

from pydantic import BaseModel, validator


class ComboBoxInfo(BaseModel):
    """
    Model representing information about a combo box.

    Attributes:
    
        current_value (str): The currently selected value in the combo box.
        current_index (int): The index of the currently selected value.
        all_options (List[str]): A list of all available options in the combo box.
        options_count (int): The total number of options available in the combo box.
    """

    current_value: str
    current_index: int
    all_options: List[str]
    options_count: int

class ComboBoxRequest(BaseModel):
    """
    Model representing a request to interact with a combo box.

    Attributes:
    
        identifier (str): The identifier of the combo box to interact with.
        index (int, optional): The index of the option to select.
        name (str, optional): The name of the option to select.

    Validators:
    
        one_of_index_or_name_must_be_provided: Ensures that either index or name is provided.
    """

    identifier: str
    index: Optional[int] = None
    name: Optional[str] = None

    @validator("index", "name", allow_reuse=True)
    def one_of_index_or_name_must_be_provided(cls, v, values):
        if v is None and values.get("index") is None and values.get("name") is None:
            raise ValueError("Either index or name must be provided")
        return v
