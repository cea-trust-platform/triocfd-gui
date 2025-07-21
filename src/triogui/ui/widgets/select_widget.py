import ipyvuetify as v
import trioapi as ta
from .object import ObjectWidget


class SelectWidget:
    def __init__(
        self, current_object, initial_type, read_object, key_path, change_list
    ):
        """
        Widget definition for Select Widget

        ----------
        Parameters

        current_object: Object
            The actual object we are dealing with

        initial_type: type
            We choose a subclass of this type to create a new object

        read_object: Object
            The initial object modified

        key_path: list
            List representing the path of the current object from the initial read object

        change_list: list
            List of all states the read object has passed through

        This widget is composed by a select to choose the type and then display widget for each attributes of the type
        """

        # Initialization
        self.current_object = current_object
        self.read_object = read_object
        self.key_path = key_path
        self.change_list = change_list
        self.initial_type = initial_type

        self.element_with_doc = []
        self.doc_dict = {}
        for element in ta.get_subclass(initial_type.__name__):
            element_name = element.__name__
            element_doc = element.__doc__
            self.element_with_doc.append(
                {"text": f"{element_name} - {element_doc}", "value": element_name}
            )
            self.doc_dict[element_name] = element_doc

        if initial_type.model_fields != {}:
            self.element_with_doc = [
                {
                    "text": f"{initial_type.__name__} - {initial_type.__doc__}",
                    "value": initial_type.__name__,
                }
            ] + self.element_with_doc
            self.doc_dict[initial_type.__name__] = initial_type.__doc__

        # We define the select with a v_model adapted
        self.select = v.Select(
            items=self.element_with_doc,
            label="Type of the attribute",
            v_model=type(current_object).__name__
            if current_object is not None
            else None,
        )

        self.doc_display = v.Alert(
            children=["Select an element to see its documentation"]
            if current_object is None
            else [self.doc_dict[type(current_object).__name__]],
            type="info",
            outlined=True,
            class_="text-body-2 pa-2 mt-2",
            style_="white-space: pre-wrap;",
        )

        # Container for dynamic widgets
        self.widget_container = v.Container()

        # If the actual object exists we create a widget with the value for it
        if self.current_object is not None and initial_type is not type(
            self.current_object
        ):
            self.widget_container.children = [
                ObjectWidget.show_widget(
                    self.current_object,
                    (type(self.current_object), False),
                    self.read_object,
                    self.key_path,
                    self.change_list,
                    True,
                )
            ]

        # Content initialization
        self.select.observe(self.change_class, "v_model")
        self.select.observe(
            lambda change, display=self.doc_display: self.update_doc(change, display),
            "v_model",
        )
        # Initial call but skip first time
        self.change_class(None, skip=True)

        selected = self.select.v_model
        if selected is not None:
            # Call show_widgets for the type selected (we instantiate the type and specify the tuple (type, is_list))
            widgets = ObjectWidget.show_widget(
                ta.trustify_gen_pyd.__dict__[selected](),
                (ta.trustify_gen_pyd.__dict__[selected], False),
                self.read_object,
                self.key_path,
                self.change_list,
                True,
            )
            self.widget_container.children = [widgets]

        self.content = v.Content(
            children=[self.select, self.doc_display, self.widget_container]
        )

    def update_doc(self, change, display_widget):
        """Updates the displayed documentation based on the selection."""
        if change and change.get("new"):
            selected_value = change["new"]
            doc_text = self.doc_dict.get(selected_value)
            display_widget.children = [doc_text]

    def change_class(self, event, skip=False):
        """
        Create the widget with the new specified type when the dropdown is modified
        """

        # Cleaning old container

        selected = self.select.v_model

        # Create adapted widget to the selectionned type but skip first time if we initially created a widget to not erase it
        if not skip:
            # Call show_widgets for the type selected (we instantiate the type and specify the tuple (type, is_list))
            widgets = ObjectWidget.show_widget(
                ta.trustify_gen_pyd.__dict__[selected](),
                (ta.trustify_gen_pyd.__dict__[selected], False),
                self.read_object,
                self.key_path,
                self.change_list,
                True,
            )
            self.widget_container.children = [widgets]
