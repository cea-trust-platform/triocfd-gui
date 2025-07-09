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

        # We define the select with a v_model adapted
        if current_object is not None:
            self.select = v.Select(
                items=[str(i.__name__) for i in ta.get_subclass(initial_type.__name__)],
                label="Type of the attribute",
                v_model=type(current_object).__name__,
            )
        else:
            self.select = v.Select(
                items=[str(i.__name__) for i in ta.get_subclass(initial_type.__name__)],
                label="Type of the attribute",
                v_model=None,
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
                )
            ]

        # Display
        self.panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=[]),
                v.ExpansionPanelContent(children=[self.widget_container]),
            ]
        )

        self.expand_panel = v.ExpansionPanels(children=[self.panel], multiple=True)

        # Content initialization
        self.select.observe(self.change_class, "v_model")

        # Initial call but skip first time
        self.change_class(None, skip=True)

        self.content = v.Content(children=[self.select, self.expand_panel])

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
            )
            self.widget_container.children = [widgets]
