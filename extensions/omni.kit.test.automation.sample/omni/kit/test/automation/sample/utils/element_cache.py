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
import uuid
from typing import Dict, Union

from ..utils.omnielement import OmniElement
from omni.kit.ui_test import WindowRef

logger = logging.getLogger("omni.kit.test.automation.sample")


class ElementCache:
    """A cache for storing OmniElements with unique identifiers."""

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.

        Parameters:
            self: The instance of the class.

        Attributes:
            element_map: A dictionary that maps string keys to OmniElement objects.
        """
        self.element_map: Dict[str, OmniElement] = {}

    def add_element(self, element: OmniElement, exists_check: bool = True) -> str:
        """
        Adds an element to the cache.

        Parameters:
            element: The element to be added to the cache.
            exists_check: A boolean value indicating whether to check for existing elements with the same realpath. Default is True.

        Returns:
            The identifier of the added element.

        Raises:
            No exceptions are explicitly raised in this function.
        """
        if exists_check:
            for existing_id, cached_element in self.element_map.items():
                if type(element) == WindowRef and element.path == cached_element.path:
                    logger.debug(
                        f"Window with path {element.path} already exists in cache with id {existing_id}"
                    )
                    return existing_id

                elif type(element) != WindowRef and element.realpath == cached_element.realpath:
                    logger.debug(
                        f"Element with path {element.path} already exists in cache with id {existing_id}"
                    )
                    return existing_id

        identifier = str(uuid.uuid4())
        self.element_map[identifier] = OmniElement(element)
        logger.debug(
            f"Added element with path {element.path} to cache with id {identifier}"
        )
        return identifier

    def get_map(self) -> Dict[str, Union[OmniElement, tuple]]:
        """
        Returns the element map.

        Returns:
            Dict[str, Union[OmniElement, tuple]]: A dictionary where keys are strings and values are either OmniElement or tuple.
        """
        return self.element_map

    def reset_map(self) -> None:
        """
        Resets the map.

        This function clears the cache of the element map.

        Parameters:
            self: The instance of the class.

        Returns:
         None.

        Raises:
            None.
        """
        logger.debug("Clearing cache")
        self.element_map.clear()

    def get_cached_element(self, identifier: str) -> OmniElement:
        """
        Retrieves a cached element using its identifier.

        Parameters:
            identifier: A string representing the unique identifier of the element.

        Returns:
            OmniElement: The cached element with the given identifier.

        Raises:
            KeyError: If the identifier is not found in the cache.
        """
        if identifier in self.element_map:
            return self.element_map[identifier]
        else:
            raise KeyError


element_cache = ElementCache()
