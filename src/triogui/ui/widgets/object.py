import ipyvuetify as v
import trioapi as ta
import inspect
from typing import get_origin, get_args, Literal
import copy
from . import (
    str_widget,
    dropdown_widget,
    float_widget,
    int_widget,
    bool_widget,
)


def set_nested_attr(obj, attr_list, value):
    if value is not None:
        for attr in attr_list[:-1]:
            if isinstance(attr, str):
                if getattr(obj, attr) is None:
                    info_class = ta.get_successive_attributes(type(obj))[attr]
                    if inspect.isclass(info_class):
                        setattr(obj, attr, info_class())
                    else:
                        setattr(
                            obj, attr, get_args(obj.model_fields[attr].annotation)[0]()
                        )
                obj = getattr(obj, attr)
            elif isinstance(attr, int):
                obj = obj[attr]
        if isinstance(attr_list[-1], str):
            setattr(obj, attr_list[-1], value)
        elif isinstance(attr_list[-1], int):
            obj[attr_list[-1]] = value


class ObjectWidget:
    def __init__(self, read_object, change_list):
        """
        Widget definition to change objects of the dataset

        Parameters
        ==========

        read_object: Pydantic object
            The object which will be modified with the widgets

        change_list: List
            List of all states the read object has passed through
        """

        # initialization
        self.read_object = read_object
        self.change_list = change_list
        self.panels = []

        # select widget to change the type of the current object
        # self.select_type = v.Select(
        #    items=[str(i) for i in ta.get_subclass(type(read_object))],
        #    label="Type",
        #    v_model=None,
        # )

        # Create recursively every widget using the attributes of the read object and the function show_widget
        for key, value in read_object.model_fields.items():
            # display description of the field
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
                children=[value.description],
            )
            header_content = v.Row(
                children=[v.Html(tag="span", children=[key], class_="mr-2"), tooltip],
                align="center",
                no_gutters=True,
            )
            panel_content = []
            # Call show_widget for each attributes
            panel_content.append(
                ObjectWidget.show_widget(
                    getattr(self.read_object, key),
                    ta.extract_true_type(value),
                    self.read_object,
                    [key],
                    self.change_list,
                )
            )
            self.panels.append(
                v.ExpansionPanel(
                    children=[
                        v.ExpansionPanelHeader(children=[header_content]),
                        v.ExpansionPanelContent(children=panel_content),
                    ]
                )
            )

        # Button to delete the last change
        self.cancel_button = v.Btn(children=["Cancel your last change"])

        # Panel and layout to display everything
        self.expand_panel = v.ExpansionPanels(children=self.panels)
        self.layout = v.Row(
            children=[
                v.Col(children=[self.cancel_button], cols=1, class_="pa-2"),
                v.Col(children=[self.expand_panel], cols=11, class_="pa-2"),
            ]
        )

        # test button to delete then
        self.test_button = v.Btn(children=["Test"])

        self.main = [self.test_button, self.layout]

    @staticmethod
    def show_widget(current_object, expected_type, read_object, key_path, change_list):
        """
        Show recursively the widget adapted to every type

        Parameters
        ==========

        current object: Object
            The current object for which the widget is created

        expected_type: tuple
            Tuple representing the type of the current object and a boolean to know if it is representing a list or not

        read_object: Object
            The initial object modified

        key_path: list
            List representing the path of the current object from the initial read object

        change_list: list
            List of all states the read object has passed through
        """

        # If the type of the current object is not a standard one (str, int, etc)
        if hasattr(expected_type[0], "model_fields") and not expected_type[1]:
            if current_object is not None:
                widget_list = []
                for key, value in current_object.model_fields.items():
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
                        children=[value.description],
                    )
                    header_content = v.Row(
                        children=[
                            v.Html(tag="span", children=[key], class_="mr-2"),
                            tooltip,
                        ],
                        align="center",
                        no_gutters=True,
                    )
                    # new widgets for each attributes of the current object
                    widget_list.append(
                        v.ExpansionPanel(
                            children=[
                                v.ExpansionPanelHeader(children=[header_content]),
                                v.ExpansionPanelContent(
                                    children=[
                                        ObjectWidget.show_widget(
                                            getattr(current_object, key),
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
                return v.ExpansionPanels(children=widget_list)

            # current object has no attributes (it is a parent class) so we create a select widget to choose the inherited class
            elif expected_type[0].model_fields == {}:
                from .select_widget import SelectWidget

                current_path = key_path
                selectw = SelectWidget(
                    expected_type[0], read_object, key_path, change_list
                )

                def change_select(event, skip_append=False):
                    if selectw.select.v_model is not None:
                        # change the read object
                        set_nested_attr(
                            read_object,
                            current_path,
                            ta.trustify_gen_pyd.__dict__[selectw.select.v_model](),
                        )
                        if not skip_append:
                            # update the list with a copy
                            change_list.append(copy.deepcopy(read_object))

                selectw.select.observe(change_select, "v_model")
                change_select(None, skip_append=True)
                return selectw.content

            else:
                widget_list = []
                # Initialize an object of the expected type to be able to modify it
                new_object = expected_type[0]()
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
                        children=[value.description],
                    )
                    header_content = v.Row(
                        children=[
                            v.Html(tag="span", children=[key], class_="mr-2"),
                            tooltip,
                        ],
                        align="center",
                        no_gutters=True,
                    )
                    # new widget list for the new object representing the expected type
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
                return v.ExpansionPanels(children=widget_list)

        # For each type that has no attributes, check its type, create the corresponding widget using its class, and update both the read object and the change list
        elif expected_type[0] is str:
            strw = str_widget.StrWidget(current_object)

            def change_str(widget, event, data):
                set_nested_attr(read_object, key_path, strw.text_str.v_model)
                change_list.append(copy.deepcopy(read_object))

            strw.text_str.on_event("blur", change_str)
            return strw.content

        elif get_origin(expected_type[0]) is Literal:
            dropdownw = dropdown_widget.DropdownWidget(
                list(get_args(expected_type[0])), current_object
            )

            def change_literal(event, skip_append=False):
                set_nested_attr(read_object, key_path, dropdownw.dropdown.v_model)
                if not skip_append:
                    change_list.append(copy.deepcopy(read_object))

            dropdownw.dropdown.observe(change_literal, "v_model")
            change_literal(None, skip_append=True)
            return dropdownw.content

        elif expected_type[0] is float:
            floatw = float_widget.FloatWidget(current_object)

            def change_float(widget, event, data):
                set_nested_attr(read_object, key_path, floatw.float_field.v_model)
                change_list.append(copy.deepcopy(read_object))

            floatw.float_field.on_event("blur", change_float)
            return floatw.content

        elif expected_type[0] is bool:
            boolw = bool_widget.BooleanWidget(current_object)

            def change_bool(event, skip_append=False):
                set_nested_attr(read_object, key_path, boolw.switch.v_model)
                if not skip_append:
                    change_list.append(copy.deepcopy(read_object))

            boolw.switch.observe(change_bool, "v_model")
            change_bool(None, skip_append=True)
            return boolw.content

        elif expected_type[0] is int:
            intw = int_widget.IntWidget(current_object)

            def change_int(widget, event, data):
                set_nested_attr(read_object, key_path, intw.number_input.v_model)
                change_list.append(copy.deepcopy(read_object))

            intw.number_input.on_event("blur", change_int)
            return intw.content

        ##elif isinstance(widget_type, list) and current_value is not None:
        ##    from .list_widget import ListWidget
        ##    current_path=key_path
        ##    listw=ListWidget(widget_type[0], current_value,read_object,key_path)
        ##
        ##    def delete_list(widget, event, data):
        ##        obj=read_object
        ##        for attr in current_path:
        ##            if isinstance(attr,str):
        ##                obj = getattr(obj, attr)
        ##            elif isinstance(attr,int):
        ##                obj=obj[attr]
        ##        obj.pop(widget.kwargs['index'])
        ##        listw.delete_item(widget.kwargs['index'])

        # for i,attr in enumerate(current_path):
        #    if i==len(current_path)-1:
        #        try:
        #            new_class= get_args(get_args(get_args(read_object[attr].model_fields.annotation)[0])[0])[0]()
        #        except TypeError:
        #            print(read_object)
        #            print(i)
        #            print(current_path)
        #            print(ta.get_successive_attributes(type(read_object)))
        #    if isinstance(attr,str):
        #        read_object = getattr(read_object, attr)
        #    elif isinstance(attr,int):
        #        read_object=read_object[attr]
        # read_object+= [new_class]
        #
        # def add_list(widget, event, data):
        #    obj=read_object
        #    for i,attr in enumerate(current_path):
        #        if i==len(current_path)-1:
        #            new_class= get_args(get_args(get_args(obj[attr].model_fields.annotation)[0])[0])[0]()
        #        if isinstance(attr,str):
        #            obj = getattr(obj, attr)
        #        elif isinstance(attr,int):
        #            obj=obj[attr]
        #    obj+= [new_class]

        # for i in listw.delete_buttons:
        #    i.on_event("click", delete_list)
        # listw.add_button.on_event("click",add_list)
        # return listw.content

        else:
            return "not defined"
