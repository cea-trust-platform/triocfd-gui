import ipyvuetify as v
import trioapi as ta
import inspect
from typing import get_origin, get_args, Literal, Union
import copy
from . import (
    str_widget,
    dropdown_widget,
    float_widget,
    int_widget,
    bool_widget,
)


def set_nested_attr(obj, attr_list, value):
    """
    Recursively sets a nested attribute in an object to a given value.

    Parameters
    ----------
    obj: object
        The root object from which the nested attribute access begins.

    attr_list: list
        A list of attribute names (str) or indices (int) indicating the path to the nested attribute.

    value: any
        The new value to assign to the final nested attribute.
    """
    if value is not None:
        for attr in attr_list[:-1]:
            if isinstance(attr, str):
                # If intermediate attribute is None, instantiate the required object
                if getattr(obj, attr) is None:
                    info_class = ta.get_successive_attributes(type(obj))[attr]
                    if inspect.isclass(info_class):
                        setattr(obj, attr, info_class())
                    else:
                        # Handle list or generic container types
                        setattr(
                            obj, attr, get_args(obj.model_fields[attr].annotation)[0]()
                        )
                obj = getattr(obj, attr)
            elif isinstance(attr, int):
                obj = obj[attr]

        # Set the final attribute (by name or index)
        if isinstance(attr_list[-1], str):
            setattr(obj, attr_list[-1], value)
        elif isinstance(attr_list[-1], int):
            obj[attr_list[-1]] = value


def get_nested_attr(obj, attr_list):
    """
    Recursively retrieves a nested attribute from an object.

    Follows a list of attribute names or indices to access and return the final nested value.

    Parameters
    ----------
    obj: object
        The root object from which the nested attribute access begins.

    attr_list: list
        A list of attribute names (str) or indices (int) indicating the path to the nested attribute.

    Returns
    -------
    any:
        The value of the final nested attribute.
    """
    for attr in attr_list:
        if isinstance(attr, str):
            obj = getattr(obj, attr)
        elif isinstance(attr, int):
            obj = obj[attr]
    return obj


class ObjectWidget:
    def __init__(self, read_object, change_list):
        """
        Widget definition to interactively modify objects in the dataset.

        ----------
        Parameters

        read_object: Pydantic object
            The object being modified. Its attributes will be rendered as editable UI fields.

        change_list: list
            A list tracking the history of changes made to `read_object`. Each change appends a deep copy.
        """

        # Store internal state
        self.read_object = read_object
        self.change_list = change_list

        # UI containers
        self.panels = []  # List of expansion panels (for nested objects)
        self.container = []  # List of flat UI cards (for basic types)

        # Tooltip for optional fields
        self.optional_tooltip = v.Tooltip(
            bottom=True,
            v_slots=[
                {
                    "name": "activator",
                    "variable": "tooltip",
                    "children": v.Icon(
                        children=["mdi-minus-circle-outline"],
                        color="green",
                        v_on="tooltip.on",
                    ),
                }
            ],
            children=["This field is optional"],
        )

        # Tooltip for required field
        self.required_tooltip = v.Tooltip(
            bottom=True,
            v_slots=[
                {
                    "name": "activator",
                    "variable": "tooltip",
                    "children": v.Icon(
                        children=["mdi-alert-circle-outline"],
                        color="orange",
                        v_on="tooltip.on",
                    ),
                }
            ],
            children=["This field is required"],
        )

        # Loop through the fields of the object to build the widget
        for key, value in read_object.model_fields.items():
            # Create a tooltip showing description and synonyms
            tooltip = v.Tooltip(
                bottom=True,
                v_slots=[
                    {
                        "name": "activator",
                        "variable": "tooltip",
                        "children": v.Icon(
                            children=["mdi-information-outline"],
                            color="blue",
                            v_on="tooltip.on",
                        ),
                    }
                ],
                children=[
                    v.Html(
                        tag="div",
                        children=[
                            v.Html(tag="div", children=["Description :"]),
                            v.Html(tag="div", children=[f"{value.description}"]),
                            v.Html(tag="div", children=["Synonyms :"]),
                            *[
                                v.Html(tag="div", children=[f"- {synonym}"])
                                for synonym in read_object._synonyms[key]
                            ],
                        ],
                    )
                ],
            )

            # Header for each attribute (field name + info icon)
            header_content = v.Row(
                children=[v.Html(tag="span", children=[key], class_="mr-2"), tooltip],
                align="center",
                no_gutters=True,
            )

            # Determine expected type (basic type or nested structure)
            expected_type = ta.extract_true_type(value)

            # Handle simple types directly (rendered as cards)
            if (
                expected_type[0] in [str, float, bool, int]
                or get_origin(expected_type[0]) is Literal
            ):
                # Verify if the attribute is declared with an Optional
                if get_origin(value.annotation) is Union:
                    header_content.children = header_content.children + [
                        self.optional_tooltip
                    ]
                else:
                    header_content.children = header_content.children + [
                        self.required_tooltip
                    ]
                self.container.append(
                    v.Card(
                        children=[
                            v.Row(
                                children=[
                                    v.Col(
                                        children=[header_content],
                                        cols=3,
                                        class_="py-1 px-2",
                                    ),
                                    v.Col(
                                        children=[
                                            ObjectWidget.show_widget(
                                                getattr(read_object, key),
                                                expected_type,
                                                self.read_object,
                                                [key],
                                                self.change_list,
                                            )
                                        ],
                                        cols=9,
                                        class_="py-1 px-2",
                                    ),
                                ],
                                class_="ma-0",
                                align="center",
                                no_gutters=True,
                            )
                        ],
                        class_="ma-1 elevation-1",
                        flat=True,
                        outlined=True,
                    )
                )

            # Handle nested types using expansion panels
            else:
                panel_content = [
                    ObjectWidget.show_widget(
                        getattr(read_object, key),
                        expected_type,
                        self.read_object,
                        [key],
                        self.change_list,
                    )
                ]
                self.panels.append(
                    v.ExpansionPanel(
                        children=[
                            v.ExpansionPanelHeader(children=[header_content]),
                            v.ExpansionPanelContent(children=panel_content),
                        ]
                    )
                )

        # Cancel button to revert the last modification
        self.cancel_button = v.Btn(children=["Cancel your last change"])

        # Final layout with editable fields and collapsible panels
        self.expand_panel = v.ExpansionPanels(children=self.panels, multiple=True)
        self.layout = v.Row(
            children=[
                v.Col(children=[self.cancel_button], cols=1, class_="pa-2"),
                v.Col(
                    children=[v.Container(children=self.container), self.expand_panel],
                    cols=11,
                    class_="pa-2",
                ),
            ]
        )

        # Store root layout
        self.main = [self.layout]

    @staticmethod
    def show_widget(
        current_object,
        expected_type,
        read_object,
        key_path,
        change_list,
        already_selected=False,
    ):
        """
        Recursively build the appropriate UI widget for any object type.

        This method dynamically generates input widgets for simple types (str, int, bool, etc.),
        expansion panels for nested objects, and custom widgets for lists and Literal types.
        It updates the `read_object` and appends changes to `change_list`.

        Parameters
        ----------
        current_object : any
            The current value of the object being rendered.

        expected_type : tuple
            A tuple with the true type of the object and a boolean indicating if it represents a list.

        read_object : object
            The top-level object being edited.

        key_path : list
            A list of attribute names/indexes tracing the path from the top-level object to the current one.

        change_list : list
            A list storing all previous states of the object to allow undoing changes.

        already_selected : bool, optional
            Used to avoid infinite recursion when rendering polymorphic types via dropdowns.
        """

        # Handle nested Pydantic objects (not lists)
        if (
            hasattr(expected_type[0], "model_fields")
            and not expected_type[1]
            and not isinstance(current_object, list)
        ):
            # If polymorphic object (multiple subclasses), render a selector widget
            if (
                ta.get_subclass(expected_type[0].__name__) != []
                and not already_selected
            ):
                from .select_widget import SelectWidget

                current_path = key_path
                selectw = SelectWidget(
                    current_object, expected_type[0], read_object, key_path, change_list
                )

                # Callback when dropdown selection changes
                def change_select(event, skip_append=False):
                    if not skip_append:
                        change_list.insert(-1, copy.deepcopy(read_object))
                        set_nested_attr(
                            read_object,
                            current_path,
                            ta.trustify_gen_pyd.__dict__[selectw.select.v_model](),
                        )

                # Observe value changes and initialize selection
                selectw.select.observe(change_select, "v_model")
                change_select(None, skip_append=True)
                return selectw.content

            # If the object is already initialized, render widgets for its fields
            elif current_object is not None:
                widget_list = []
                container = []

                # Loop through each attribute in the object
                for key, value in current_object.model_fields.items():
                    # Build a tooltip for help info
                    tooltip = v.Tooltip(
                        bottom=True,
                        v_slots=[
                            {
                                "name": "activator",
                                "variable": "tooltip",
                                "children": v.Icon(
                                    children=["mdi-information-outline"],
                                    color="blue",
                                    v_on="tooltip.on",
                                ),
                            }
                        ],
                        children=[
                            v.Html(
                                tag="div",
                                children=[
                                    v.Html(tag="div", children=["Description :"]),
                                    v.Html(
                                        tag="div", children=[f"{value.description}"]
                                    ),
                                    v.Html(tag="div", children=["Synonyms :"]),
                                    *[
                                        v.Html(tag="div", children=[f"- {synonym}"])
                                        for synonym in current_object._synonyms[key]
                                    ],
                                ],
                            ),
                        ],
                    )

                    # Tooltip for optional fields
                    optional_tooltip = v.Tooltip(
                        bottom=True,
                        v_slots=[
                            {
                                "name": "activator",
                                "variable": "tooltip",
                                "children": v.Icon(
                                    children=["mdi-minus-circle-outline"],
                                    color="green",
                                    v_on="tooltip.on",
                                ),
                            }
                        ],
                        children=["This field is optional"],
                    )

                    # Tooltip for required field
                    required_tooltip = v.Tooltip(
                        bottom=True,
                        v_slots=[
                            {
                                "name": "activator",
                                "variable": "tooltip",
                                "children": v.Icon(
                                    children=["mdi-alert-circle-outline"],
                                    color="orange",
                                    v_on="tooltip.on",
                                ),
                            }
                        ],
                        children=["This field is required"],
                    )

                    header_content = v.Row(
                        children=[
                            v.Html(tag="span", children=[key], class_="mr-2"),
                            tooltip,
                        ],
                        align="center",
                        no_gutters=True,
                    )

                    expected_type = ta.extract_true_type(value)

                    # If simple type, create inline card
                    if (
                        expected_type[0] in [str, float, bool, int]
                        or get_origin(expected_type[0]) is Literal
                    ):
                        # Verify if the attribute is declared with an Optional
                        if get_origin(value.annotation) is Union:
                            header_content.children = header_content.children + [
                                optional_tooltip
                            ]
                        else:
                            header_content.children = header_content.children + [
                                required_tooltip
                            ]

                        container.append(
                            v.Card(
                                children=[
                                    v.Row(
                                        children=[
                                            v.Col(
                                                children=[header_content],
                                                cols=3,
                                                class_="py-0 px-1",
                                            ),
                                            v.Col(
                                                children=[
                                                    ObjectWidget.show_widget(
                                                        getattr(current_object, key),
                                                        expected_type,
                                                        read_object,
                                                        key_path + [key],
                                                        change_list,
                                                    )
                                                ],
                                                cols=9,
                                                class_="py-0 px-0",
                                            ),
                                        ],
                                        class_="ma-0",
                                        align="center",
                                        no_gutters=True,
                                        style="height: 5px; line-height: 5px; font-size: 5px;",
                                    )
                                ],
                                class_="ma-1 elevation-1",
                                flat=True,
                                outlined=True,
                                style="height: 12px; line-height: 12px; font-size: 8px;",
                            )
                        )

                    # Otherwise, create expansion panel for nested attributes
                    else:
                        widget_list.append(
                            v.ExpansionPanel(
                                children=[
                                    v.ExpansionPanelHeader(children=[header_content]),
                                    v.ExpansionPanelContent(
                                        children=[
                                            ObjectWidget.show_widget(
                                                getattr(current_object, key),
                                                expected_type,
                                                read_object,
                                                key_path + [key],
                                                change_list,
                                            )
                                        ]
                                    ),
                                ]
                            )
                        )

                expand_panel = v.ExpansionPanels(children=widget_list, multiple=True)
                return v.Container(
                    children=[v.Container(children=container), expand_panel]
                )

            # If the object is None and has no subclasses, offer to initialize
            else:
                panel = v.ExpansionPanels(children=[])
                initialize = v.Btn(
                    color="red",
                    children=["Initialize"],
                )

                def initialize_object(widget, event, data):
                    new_object = expected_type[0]()
                    widget_list = []

                    for key, value in new_object.model_fields.items():
                        tooltip = v.Tooltip(
                            bottom=True,
                            v_slots=[
                                {
                                    "name": "activator",
                                    "variable": "tooltip",
                                    "children": v.Icon(
                                        children=["mdi-information-outline"],
                                        color="blue",
                                        v_on="tooltip.on",
                                    ),
                                }
                            ],
                            children=[
                                v.Html(
                                    tag="div",
                                    children=[
                                        v.Html(tag="div", children=["Description :"]),
                                        v.Html(
                                            tag="div", children=[f"{value.description}"]
                                        ),
                                        v.Html(tag="div", children=["Synonyms :"]),
                                        *[
                                            v.Html(tag="div", children=[f"- {synonym}"])
                                            for synonym in new_object._synonyms[key]
                                        ],
                                    ],
                                ),
                            ],
                        )

                        header_content = v.Row(
                            children=[
                                v.Html(tag="span", children=[key], class_="mr-2"),
                                tooltip,
                            ],
                            align="center",
                            no_gutters=True,
                        )

                        widget_list.append(
                            v.ExpansionPanel(
                                children=[
                                    v.ExpansionPanelHeader(children=[header_content]),
                                    v.ExpansionPanelContent(
                                        children=[
                                            ObjectWidget.show_widget(
                                                getattr(new_object, key),
                                                ta.extract_true_type(value),
                                                read_object,
                                                key_path + [key],
                                                change_list,
                                            )
                                        ]
                                    ),
                                ]
                            )
                        )

                    panel.children = widget_list
                    change_list.insert(-1, copy.deepcopy(read_object))
                    set_nested_attr(read_object, key_path, new_object)

                panel.children = [initialize]
                initialize.on_event("click", initialize_object)
                return v.Container(children=[panel])

        # If the field is a list (expected_type[1] is True) or an actual list instance
        elif (
            expected_type[1] or isinstance(current_object, list)
        ) and current_object is not None:
            from .list_widget import ListWidget

            current_path = key_path

            # Create a custom widget for list handling
            listw = ListWidget(
                current_object, expected_type[0], read_object, key_path, change_list
            )

            # Callback to delete an item from the list
            def delete_list(widget, event, data):
                updated_object = get_nested_attr(read_object, key_path)
                index = widget.kwargs["index"]
                updated_object.pop(index)

                set_nested_attr(read_object, key_path, updated_object)
                change_list.insert(-1, copy.deepcopy(read_object))

                listw.build_panels(updated_object)
                for btn in listw.delete_buttons:
                    btn.on_event("click", delete_list)
                for btn in listw.duplicate_buttons:
                    btn.on_event("click", duplicate_list)

            # Callback to add a new (empty) item to the list
            def add_list(widget, event, data):
                updated_object = get_nested_attr(read_object, key_path)
                updated_object.append(copy.deepcopy(expected_type[0]()))
                set_nested_attr(read_object, key_path, updated_object)
                change_list.insert(-1, copy.deepcopy(read_object))

                listw.build_panels(updated_object)
                for btn in listw.delete_buttons:
                    btn.on_event("click", delete_list)
                for btn in listw.duplicate_buttons:
                    btn.on_event("click", duplicate_list)

            # Callback to duplicate an item in the list
            def duplicate_list(widget, event, data):
                updated_object = get_nested_attr(read_object, key_path)
                index = widget.kwargs["index"]
                updated_object.append(copy.deepcopy(updated_object[index]))
                set_nested_attr(read_object, key_path, updated_object)
                change_list.insert(-1, copy.deepcopy(read_object))

                listw.build_panels(updated_object)
                for btn in listw.delete_buttons:
                    btn.on_event("click", delete_list)
                for btn in listw.duplicate_buttons:
                    btn.on_event("click", duplicate_list)

            # Register events on buttons
            for i in listw.delete_buttons:
                i.on_event("click", delete_list)
            for i in listw.duplicate_buttons:
                i.on_event("click", duplicate_list)

            listw.add_button.on_event("click", add_list)

            return listw.content

        # Handle primitive types (non-nested attributes)
        elif expected_type[0] is str:
            strw = str_widget.StrWidget(current_object)

            def change_str(widget, event, data):
                change_list.insert(-1, copy.deepcopy(read_object))
                set_nested_attr(read_object, key_path, strw.text_str.v_model)

            strw.text_str.on_event("blur", change_str)
            return strw.content

        elif get_origin(expected_type[0]) is Literal:
            dropdownw = dropdown_widget.DropdownWidget(
                list(get_args(expected_type[0])), current_object
            )

            def change_literal(event, skip_append=False):
                if not skip_append:
                    change_list.insert(-1, copy.deepcopy(read_object))
                    set_nested_attr(read_object, key_path, dropdownw.dropdown.v_model)

            dropdownw.dropdown.observe(change_literal, "v_model")
            change_literal(None, skip_append=True)
            return dropdownw.content

        elif expected_type[0] is float:
            floatw = float_widget.FloatWidget(current_object)

            def change_float(widget, event, data):
                change_list.insert(-1, copy.deepcopy(read_object))
                set_nested_attr(
                    read_object, key_path, float(floatw.float_field.v_model)
                )

            floatw.float_field.on_event("blur", change_float)
            return floatw.content

        elif expected_type[0] is bool:
            boolw = bool_widget.BooleanWidget(current_object)

            def change_bool(event, skip_append=False):
                if not skip_append:
                    change_list.insert(-1, copy.deepcopy(read_object))
                    set_nested_attr(read_object, key_path, boolw.switch.v_model)

            boolw.switch.observe(change_bool, "v_model")
            change_bool(None, skip_append=True)
            return boolw.content

        elif expected_type[0] is int:
            intw = int_widget.IntWidget(current_object)

            def change_int(widget, event, data):
                change_list.insert(-1, copy.deepcopy(read_object))
                set_nested_attr(read_object, key_path, int(intw.number_input.v_model))

            intw.number_input.on_event("blur", change_int)
            return intw.content

        # If the list is uninitialized (None), offer an "Initialize" button
        elif current_object is None and expected_type[1]:
            container = v.Container(children=[])
            initialize = v.Btn(
                color="red",
                children=["Initialize"],
            )

            def initialize_object(widget, event, data):
                new_object = expected_type[0]()
                widget = ObjectWidget.show_widget(
                    [new_object],
                    expected_type,
                    read_object,
                    key_path,
                    change_list,
                )

                container.children = [widget]
                change_list.insert(-1, copy.deepcopy(read_object))
                set_nested_attr(read_object, key_path, [new_object])

            container.children = [initialize]
            initialize.on_event("click", initialize_object)

            return container

        # Catch-all for unknown or unhandled types
        else:
            return f"{current_object} [[]]{expected_type}"
