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
from typing import Any, Tuple, Union

import omni.appwindow
import omni.kit.ui_test as ui_test
from carb.input import MouseEventType
from omni import ui
from omni.kit.ui_test.input import (
    emulate_mouse_move_and_click,
    emulate_mouse,
    human_delay,
    emulate_mouse_click,
)
from omni.kit.ui_test.query import WidgetRef
from omni.kit.ui_test.vec2 import Vec2


logger = logging.getLogger("kit_control")


async def wrapper_function(event_type: MouseEventType, pos: Vec2 = Vec2()):
    """
    A wrapper function for emulating a mouse event.

    This function is a wrapper around the `emulate_mouse_without_cursor` function.
    It is used to emulate a mouse event of the given type at the specified position.

    Parameters:
        event_type (MouseEventType): The type of the mouse event.
        pos (Vec2, optional): The position of the mouse event. Defaults to Vec2().

    Returns:
        None
    """
    await emulate_mouse_without_cursor(event_type, pos)


async def emulate_mouse_without_cursor(event_type: MouseEventType, pos: Vec2 = Vec2()):
    """
    Emulate a mouse event without a cursor specifically implemented for APPs running in headless mode like in OVC.

    This function is used to emulate a mouse event of the given type at the
    specified position. It does not require a physical cursor and can be used
    to simulate mouse events in a headless environment.

    Parameters:
        event_type (MouseEventType): The type of the mouse event.
        pos (Vec2, optional): The position of the mouse event. Defaults to Vec2().

    Returns:
        None
    """
    app_window = omni.appwindow.get_default_app_window()
    mouse = app_window.get_mouse()
    window_width = ui.Workspace.get_main_window_width()
    window_height = ui.Workspace.get_main_window_height()
    pos = pos * ui.Workspace.get_dpi_scale()
    ui_test.input._get_input_provider().buffer_mouse_event(
        mouse,
        event_type,
        (pos.x / window_width, pos.y / window_height),
        0,
        pos.to_tuple(),
    )


async def emulate_mouse_move_and_click(
    pos: Vec2, right_click=False, double=False, human_delay_speed: int = 2
):
    """Emulate Mouse move into position and click."""
    logger.info(
        f"emulate_mouse_move_and_click pos: {pos} (right_click: {right_click}, double: {double})"
    )
    await emulate_mouse(MouseEventType.MOVE, pos)
    await human_delay(human_delay_speed)
    await emulate_mouse_click(right_click=right_click, double=double)
    await human_delay(human_delay_speed)


ui_test.input.emulate_mouse = wrapper_function


class OmniElement(WidgetRef):
    """
    A class representing a UI element in an Omni application.

    This class extends the `WidgetRef` class and provides additional properties and methods to interact with the UI element.

    Attributes:
        element (ui_test.WidgetRef): The underlying `WidgetRef` object representing the UI element.

    Methods:
        __init__(self, element: ui_test.WidgetRef) -> None:
            Initializes the `OmniElement` object with the given `WidgetRef` object.

        name(self) -> str:
            Returns the name of the UI element.

        visible(self) -> bool:
            Returns whether the UI element is visible or not.

        enabled(self) -> bool:
            Returns whether the UI element is enabled or not.

        width(self) -> Union[float, Tuple[int, str]]:
            Returns the width of the UI element.

        height(self) -> Union[float, Tuple[int, str]]:
            Returns the height of the UI element.

        str_value(self) -> str:
            Returns the string value of the UI element.

        int_value(self) -> int:
            Returns the integer value of the UI element.

        float_value(self) -> float:
            Returns the float value of the UI element.

        bool_value(self) -> bool:
            Returns the boolean value of the UI element.

        get_type(self) -> str:
            Returns the type of the UI element.

        collapsed(self) -> Union[bool, Tuple[int, str]]:
            Returns whether the UI element is collapsed or not.

        slider_range(self) -> Union[Tuple[float, float], Tuple[int, str]]:
            Returns the minimum and maximum values of a slider UI element.

        center(self) -> Union[Tuple[float, float], Tuple[int, str]]:
            Returns the center position of the UI element.

        text(self) -> Union[str, Tuple[int, str]]:
            Returns the text value of the UI element.

        selected(self) -> Union[bool, Tuple[int, str]]:
            Returns whether the UI element is selected or not.

        checked(self) -> Union[bool, Tuple[int, str]]:
            Returns whether the UI element is checked or not.

        dock(self) -> Union[Tuple[bool, int, int], Tuple[int, str]]:
            Returns the dock status, order, and ID of the UI element.

        value(self) -> Union[Any, Tuple[int, str]]:
            Returns the value of the UI element.

        alignment(self) -> Union[Any, Tuple[int, str]]:
            Returns the alignment of the UI element.

        canvas(self) -> Union[Tuple[float, float, float, float], Tuple[int, str]]:
            Returns the zoom, pan_x, and pan_y values of a canvas UI element.

        screen_position_x(self) -> Union[float, Tuple[int, str]]:
            Returns the x-coordinate of the screen position of the UI element.

        screen_position_y(self) -> Union[float, Tuple[int, str]]:
            Returns the y-coordinate of the screen position of the UI element.

        change_height(self, value: float):
            Changes the height of the UI element.

        change_width(self, value: float):
            Changes the width of the UI element.

        bring_to_front(self, undock: bool = False):
            Brings the window containing the UI element to the front.

        click(self, bring_to_front: bool = True, pos: Vec2 = None, right_click=False, double=False, human_delay_speed: int = 2):
            Emulates a mouse click on the UI element.
    """

    def __init__(self, element: ui_test.WidgetRef) -> None:
        """
        Initializes the instance with a given widget reference.

        Parameters:
        element: A reference to the widget.

        Raises:
        TypeError: If the provided element is not a ui_test.WidgetRef."""
        super().__init__(element.widget, element.path)

    @property
    def name(self) -> str:
        """
        Retrieves the name of the widget.

        Returns:
            The name of the widget as a string.

        Raises:
            AttributeError: If the 'enabled' attribute is not found on the widget or window.
        """
        try:
            return self.widget.name
        except AttributeError:
            message = (
                f"The 'name' not found on the {self.get_type} at path {self.path}."
            )
            logger.error(message)
            return message

    @property
    def visible(self) -> bool:
        """
        Returns the visibility status of the widget.

        Returns:
            bool: True if the widget is visible, False otherwise.
        """
        return self.widget.visible

    @property
    def enabled(self) -> bool:
        """
        Gets the enabled status of the widget.

        Returns:
            bool: True if the widget is enabled, False otherwise.

        Raises:
            AttributeError: If the 'enabled' attribute is not found on the widget or window.
        """

        try:
            return self.widget.enabled
        except AttributeError:
            message = (
                f"The 'enabled' not found on the {self.get_type} at path {self.path}."
            )
            logger.error(message)
            return message

    @property
    def width(self) -> Union[float, Tuple[int, str]]:
        """
        Gets the width of the widget or window.

        Returns:
            float or Tuple[int, str]: The width of the widget or window, or an error message if the attribute is not found.

        Raises:
            AttributeError: If the 'width' attribute is not found on the widget or window.
        """
        try:
            if "window" not in str(type(self.widget)).lower():
                return self.widget.computed_width
            else:
                return self.window.width
        except Exception:
            message = f"The 'width' attribute is not found on the {self.get_type} at path {self.path}."
            logger.error(message)
            return message

    @property
    def height(self) -> Union[float, Tuple[int, str]]:
        """
        Gets the height of the widget or window.

        Returns:
            - If the widget is not a window, returns the computed content height of the widget.
            - If the widget is a window, returns the height of the window.
            - If the height attribute is not found, returns a tuple containing an error code and a message.

        Raises:
            - An error message is logged if the height attribute is not found.
        """
        try:
            if "window" not in str(type(self.widget)).lower():
                return self.widget.computed_content_height
            else:
                return self.window.height
        except Exception:
            message = f"The 'height' attribute is not found on the {self.get_type} at path {self.path}."
            logger.error(message)
            return message

    @property
    def str_value(self) -> str:
        """
        Retrieves the value as a string.

        Returns:
            The value as a string.

        Raises:
            AttributeError: If the 'model' attribute is not found.
        """
        try:
            return self.model.get_value_as_string()
        except AttributeError:
            message = f"The 'str_value' attribute requires 'model' attribute to be present which is not found on the {self.get_type} at path {self.path}."
            logger.error(message)
            return message

    @property
    def int_value(self) -> int:
        """
        Retrieves the integer value from the model.

        Returns:
            The integer value from the model.

        Raises:
            AttributeError: If the 'model' attribute is not found on the object.
        """
        try:
            return self.model.get_value_as_int()
        except AttributeError:
            message = f"The 'int_value' attribute requires 'model' attribute to be present which is not found on the {self.get_type} at path {self.path}."
            logger.error(message)
            return message

    @property
    def float_value(self) -> float:
        """
        Retrieves the value as a float.

        Returns:
            The value as a float.

        Raises:
            AttributeError: If the 'model' attribute is not found.
        """
        try:
            return self.model.get_value_as_float()
        except AttributeError:
            message = f"The 'float_value' attribute requires 'model' attribute to be present which is not found on the {self.get_type} at path {self.path}."
            logger.error(message)
            return message

    @property
    def bool_value(self) -> float:
        """
        Retrieves the boolean value from the model.

        Returns:
            The boolean value if successful, otherwise an error tuple.

        Raises:
            AttributeError: If the 'model' attribute is not found.
        """
        try:
            return self.model.get_value_as_bool()
        except AttributeError:
            message = f"The 'bool_value' attribute requires 'model' attribute to be present which is not found on the {self.get_type} at path {self.path}."
            logger.error(message)
            return message

    @property
    def get_type(self) -> str:
        """
        Returns the type of the widget as a string.

        Returns:
            str: The type of the widget.
        """
        return str(self.widget.__class__.__name__)

    @property
    def collapsed(self) -> Union[bool, Tuple[int, str]]:
        """
        Retrieves the collapsed state of the widget.

        Returns:
            bool or Tuple[int, str]: The collapsed state of the widget if found, otherwise an error tuple.

        Raises:
            AttributeError: If the 'collapsed' attribute is not found on the widget.
        """
        try:
            return self.widget.collapsed
        except AttributeError:
            message = f"The 'collapsed' attribute is not found on the {self.get_type} at path {self.path}."
            logger.error(message)
            return message

    @property
    def slider_range(self) -> Union[Tuple[float, float], Tuple[int, str]]:
        """
        Retrieves the range of the slider.

        Returns:
            A tuple containing the minimum and maximum values of the slider, or an error message if the attributes are not found.

        Raises:
            AttributeError: If the 'min' or 'max' attributes are not found on the widget.
        """
        try:
            min = self.widget.min
            max = self.widget.max
        except AttributeError:
            try:
                min = self.widget.delegate._SliderMenuDelegate__slider.min
                max = self.widget.delegate._SliderMenuDelegate__slider.max
            except AttributeError:
                message = f"The 'min, max' attributes are not found on the {self.get_type} at path {self.path}."
                logger.error(message)
                return message
        return (min, max)

    @property
    def center(self) -> Union[Tuple[float, float], Tuple[int, str]]:
        """
        Calculates and returns the center of the object.

        Returns:
            Tuple[float, float]: The center coordinates of the object.
            Tuple[int, str]: An error code and message if the 'center' attribute is not found.

        Raises:
            AttributeError: If the 'center' attribute is not found on the object.
        """
        try:
            return self.position + self.size / 2
        except AttributeError:
            message = f"The 'center' attribute is not found on the {self.get_type} at path {self.path}."
            logger.error(message)
            return message

    @property
    def text(self) -> Union[str, Tuple[int, str]]:
        """
        Retrieves the text attribute of the widget.

        Returns:
            str or Tuple[int, str]: The text attribute of the widget, or an error message if the attribute is not found.

        Raises:
            AttributeError: If the text attribute is not found on the widget.
        """
        try:
            return self.widget.text
        except AttributeError:
            try:
                return self.str_value
            except AttributeError:
                message = f"The 'text' attribute is not found on the {self.get_type} at path {self.path}."
                logger.error(message)
                return message

    @property
    def selected(self) -> Union[bool, Tuple[int, str]]:
        """
        Gets the selected value of the widget or boolean value.

        Returns:
            A boolean value or a tuple containing an error code and message if an attribute error occurs.

        Raises:
            AttributeError: If the 'selected' attribute is not found on the widget or the 'bool_value' attribute is not found.
        """
        try:
            return self.widget.selected
        except AttributeError:
            try:
                return self.bool_value
            except AttributeError:
                message = f"The 'text' attribute is not found on the {self.get_type} at path {self.path}."
                logger.error(message)
                return message

    @property
    def checked(self) -> Union[bool, Tuple[int, str]]:
        """
        Gets the checked attribute of the widget.

        Returns:
            bool: The checked attribute of the widget.
            Tuple[int, str]: An error code and message if the attribute is not found.

        Raises:
            AttributeError: If the attribute is not found.
        """
        try:
            return self.widget.checked
        except AttributeError:
            try:
                return self.bool_value
            except AttributeError:
                message = f"The 'checked' attribute is not found on the {self.get_type} at path {self.path}."
                logger.error(message)
                return message

    @property
    def dock(self) -> Union[Tuple[bool, int, int], Tuple[int, str]]:
        """
        Retrieves the dock status, order, and ID.

        Returns:
            A tuple containing the dock status (bool), order (int), and ID (int) if successful.
            A tuple containing an error code (int) and a message (str) if an AttributeError occurs.

        Raises:
            AttributeError: If the 'dock' attribute is not found on the object.
        """
        try:
            dock_status = self.window.docked
            dock_order = self.window.dock_order
            dock_id = self.window.dock_id
            return (dock_status, dock_order, dock_id)
        except AttributeError:
            message = f"The 'dock' attribute is not found on the {self.get_type} at path {self.path}."
            logger.error(message)
            return message

    @property
    def value(self) -> Union[Any, Tuple[int, str]]:
        """
        Retrieves the value of the widget.

        Returns:
            The value of the widget if it exists, otherwise returns a tuple containing an error code and a message.

        Raises:
            AttributeError: If the 'value' attribute is not found on the widget.
        """
        try:
            return self.widget.value()
        except AttributeError:
            message = f"The 'value' attribute is not found on the {self.get_type} at path {self.path}."
            logger.error(message)
            return message

    @property
    def alignment(self) -> Union[Any, Tuple[int, str]]:
        """
        Gets the alignment of the widget.

        Returns:
            The alignment of the widget if found, otherwise returns an error code and message.

        Raises:
            AttributeError: If the 'alignment' attribute is not found on the widget.
        """
        try:
            return self.widget.alignment
        except AttributeError:
            message = f"The 'alignment' attribute is not found on the {self.get_type} at path {self.path}."
            logger.error(message)
            return message

    @property
    def canvas(self) -> Union[Tuple[float, float, float, float], Tuple[int, str]]:
        """
        Returns the canvas properties of the widget.

        Returns:
            - If the widget is a CanvasFrame, returns a tuple containing zoom, pan_x, and pan_y.
            - If the widget is not a CanvasFrame, returns a tuple containing an error code and a message.

        Raises:
            - None
        """
        if type(self.widget) == ui.CanvasFrame:
            zoom = self.widget.zoom
            pan_x = self.widget.pan_x
            pan_y = self.widget.pan_y
            return (zoom, pan_x, pan_y)
        else:
            message = f"The 'canvas properties' attribute is not found on the {self.get_type} at path {self.path}."
            logger.error(message)
            return message

    @property
    def screen_position_x(self) -> Union[float, Tuple[int, str]]:
        """
        Gets the screen position x of the widget.

        Returns:
            float: The screen position x of the widget.
            Tuple[int, str]: A tuple containing an error code and a message if the attribute is not found.

        Raises:
            AttributeError: If the 'screen_position_x' attribute is not found on the widget.
        """
        try:
            return self.widget.screen_position_x
        except Exception:
            message = f"The 'screen_position_x' attribute is not found on the {self.get_type} at path {self.path}."
            logger.error(message)
            return message

    @property
    def screen_position_y(self) -> Union[float, Tuple[int, str]]:
        """
        Gets the screen position y of the widget.

        Returns:
            float: The screen position y of the widget.
            Tuple[int, str]: A tuple containing an error code and a message if the attribute is not found.

        Raises:
            AttributeError: If the 'screen_position_y' attribute is not found on the widget.
        """
        try:
            return self.widget.screen_position_y
        except Exception:
            message = f"The 'screen_position_y' attribute is not found on the {self.get_type} at path {self.path}."
            logger.error(message)
            return message

    @property
    def widget_position(self):
        """
        Gets the position of the widget.

        Returns:
            Tuple[int, int]: A tuple containing the x and y coordinates of the widget's position.

        Raises:
            AttributeError: If the 'position' attribute is not found on the widget.
        """
        try:
            self.position.to_tuple()
        except Exception:
            message = f"The 'position' attribute is not found on the {self.get_type} at path {self.path}."
            logger.error(message)
            return message

    @property
    def widget_size(self):
        """
        Gets the size of the widget.

        Returns:
            Tuple[int, int]: A tuple containing the width and height of the widget's size.

        Raises:
            AttributeError: If the 'size' attribute is not found on the widget.
        """
        try:
            self.size.to_tuple()
        except Exception:
            message = f"The 'size' attribute is not found on the {self.get_type} at path {self.path}."
            logger.error(message)
            return message

    def change_height(self, value: float):
        """
        Changes the height of the widget.

        Parameters:
            value (float): The new height value.

        Raises:
            TypeError: If the provided value is not a float.
            ValueError: If the provided value is less than or equal to zero.
        """
        self.widget.height = value

    def change_width(self, value: float):
        """
        Changes the width of the widget.

        Parameters:
            value (float): The new width value.

        Raises:
            TypeError: If the provided value is not a float.
            ValueError: If the provided value is less than or equal to zero.
        """
        self.widget.width = value

    async def bring_to_front(self, undock: bool = False):
        """
        Bring window this widget belongs to on top. Currently this is implemented as conditional undock() + focus().
        """
        if undock:
            await self.undock()
        await self.focus()

    async def click(
        self,
        bring_to_front: bool = True,
        pos: Vec2 = None,
        right_click=False,
        double=False,
        human_delay_speed: int = 2,
    ):
        """
        Emulate mouse click on the widget."""
        if bring_to_front:
            await self.bring_to_front()
        if not pos:
            if self.enabled and self.visible:
                pos = self.center
        await emulate_mouse_move_and_click(
            pos,
            right_click=right_click,
            double=double,
            human_delay_speed=human_delay_speed,
        )

    def get_properties(self):
        """
        Returns the properties of the object.

        Returns:
            A dictionary containing the following properties:
            - name: The name of the object.
            - visible: Whether the object is visible or not.
            - enabled: Whether the object is enabled or not.
            - height: The height of the object.
            - width: The width of the object.
            - str_value: The string value of the object.
            - int_value: The integer value of the object.
            - float_value: The float value of the object.
            - bool_value: The boolean value of the object.
            - get_type: The type of the object.
            - collapsed: Whether the object is collapsed or not.
            - slider_range: The range of the slider of the object.
            - center: The center of the object as a tuple.
            - text: The text of the object.
            - selected: Whether the object is selected or not.
            - checked: Whether the object is checked or not.
            - dock: The docking position of the object.
            - value: The value of the object.
            - canvas: The canvas of the object.
            - screen_position_x: The x-coordinate of the object on the screen.
            - screen_position_y: The y-coordinate of the object on the screen.
            - path: The path of the object.
            - real_path: The real path of the object.
            - position: The position of the object as a tuple.
            - size: The size of the object as a tuple."""
        properties = {
            "name": self.name,
            "visible": self.visible,
            "enabled": self.enabled,
            "height": self.height,
            "width": self.width,
            "str_value": self.str_value,
            "int_value": self.int_value,
            "float_value": self.float_value,
            "bool_value": self.bool_value,
            "get_type": self.get_type,
            "collapsed": self.collapsed,
            "slider_range": self.slider_range,
            "center": self.center,
            "text": self.text,
            "selected": self.selected,
            "checked": self.checked,
            "dock": self.dock,
            "value": self.value,
            "canvas": self.canvas,
            "screen_position_x": self.screen_position_x,
            "screen_position_y": self.screen_position_y,
            "path": str(self.path) or "",
            "real_path": str(self.realpath) or "",
            "position": self.widget_position,
            "size": self.widget_size,
        }

        return properties
