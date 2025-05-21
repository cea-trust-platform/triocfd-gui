import ipyvuetify as v
import trioapi as ta
import inspect
from typing import get_origin, get_args, Literal
from . import (
    str_widget,
    dropdown_widget,
    float_widget,
    int_widget,
    bool_widget,
)


class ObjectWidget:
    def __init__(self, read_object):
        """
        Widget definition to change objects of the dataset

        Parameters
        ==========

        read_object: Pydantic object
            The object which will be modified with the widgets

         :Explanation
        """

        # collect information on every type of the object and the attributes
        self.list_type = ta.obj_to_dict_type(read_object)
        self.dict_type = ta.get_successive_attributes(type(read_object))

        # widget to select to change the type of the current object
        self.select_type = v.Select(
            items=[str(i) for i in ta.get_subclass(self.list_type[0].__name__)],
            label="Type",
            v_model=None,
        )

        self.panels = []

        # Create widgets recurively using the dict contained in the list (1st index is the type and the second is the dict of the attributes)
        for key, value in self.list_type[1].items():
            panel_content = []
            # if the value is None for the current object we create a widget with the type of the object kept in the dict
            if value is None:
                panel_content.append(
                    ObjectWidget.show_widget(self.dict_type[key], value)
                )
            else:
                panel_content.append(
                    ObjectWidget.show_widget(self.dict_type[key], value)
                )
            self.panels.append(
                v.ExpansionPanel(
                    children=[
                        v.ExpansionPanelHeader(children=[key]),
                        v.ExpansionPanelContent(children=panel_content),
                    ]
                )
            )

        self.expand_panel = v.ExpansionPanels(children=self.panels)
        self.main = [self.select_type, self.expand_panel]

    @staticmethod
    def show_widget(widget_type, current_value):
        """
        Show recursively the widget adapted to every type

        Parameters
        ==========

        widget_type: type
            The type (or the dict of type for every attributes) for which we want to create a widget

        current_value: ?
            The current value in the actual dataset
        """

        # Original attribute is None and a class sow e crate a widget to create the attributes from zero
        if isinstance(widget_type, dict) and current_value is None:
            widget_list = []
            for key, value in widget_type.items():
                widget_list.append(
                    v.ExpansionPanel(
                        children=[
                            v.ExpansionPanelHeader(children=[key]),
                            v.ExpansionPanelContent(
                                children=[ObjectWidget.show_widget(value, None)]
                            ),
                        ]
                    )
                )
            return v.ExpansionPanels(children=widget_list)

        # Orignal attribute has a value so we create a widget with every of its attributes
        elif isinstance(widget_type, dict):
            widget_list = []
            for key, value in widget_type.items():
                widget_list.append(
                    v.ExpansionPanel(
                        children=[
                            v.ExpansionPanelHeader(children=[key]),
                            v.ExpansionPanelContent(
                                children=[
                                    ObjectWidget.show_widget(
                                        value, current_value[1][key]
                                    )
                                ]
                            ),
                        ]
                    )
                )
            return v.ExpansionPanels(children=widget_list)

        elif (
            inspect.isclass(widget_type)
            and hasattr(ta, widget_type.__name__)
            and current_value is None
        ):
            from .select_widget import SelectWidget

            return SelectWidget(widget_type).content

        elif (
            inspect.isclass(widget_type)
            and hasattr(ta, widget_type.__name__)
            and current_value is not None
        ):
            return ObjectWidget.show_widget(
                ta.get_successive_attributes(current_value[0]), current_value
            )

        elif widget_type is str:
            return str_widget.StrWidget(current_value).content

        elif get_origin(widget_type) is Literal:
            return dropdown_widget.DropdownWidget(
                list(get_args(widget_type)), current_value
            ).content

        elif widget_type is float:
            return float_widget.FloatWidget(current_value).content

        elif widget_type is bool:
            return bool_widget.BooleanWidget(current_value).content

        elif widget_type is int:
            return int_widget.IntWidget(current_value).content

        elif isinstance(widget_type, list) and current_value is not None:
            from .list_widget import ListWidget

            return ListWidget(widget_type[0], current_value).content

        else:
            return "not defined"
