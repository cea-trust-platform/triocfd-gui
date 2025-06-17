import ipyvuetify as v
import trioapi as ta
from .object import ObjectWidget


class SelectWidget:
    def __init__(self, initial_type, read_object, key_path, change_list):
        """
        Widget definition for Select Widget

        ----------
        Parameters

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
        self.read_object = read_object
        self.key_path = key_path
        self.change_list = change_list
        self.select = v.Select(
            items=[str(i.__name__) for i in ta.get_subclass(initial_type.__name__)],
            label="Type of the attribute",
            v_model=None,
        )

        # Container for dynamic widgets
        self.widget_container = v.Container()

        self.panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=[]),
                v.ExpansionPanelContent(children=[self.widget_container]),
            ]
        )

        self.expand_panel = v.ExpansionPanels(children=[self.panel])

        # Content initialization
        self.select.observe(self.change_class, "v_model")
        # Initial call
        self.change_class(None)

        self.content = v.Content(children=[self.select, self.expand_panel])

    def change_class(self, event):
        """
        Create the widget with the new specified type when the dropdown is modified
        """

        # Cleaning old container
        self.widget_container.children = []

        selected = self.select.v_model
        if selected:
            # Call show_widgets for the type selected (we instantiate the type and specify the tuple (type, is_list))
            widgets = ObjectWidget.show_widget(
                ta.trustify_gen_pyd.__dict__[selected](),
                (ta.trustify_gen_pyd.__dict__[selected], False),
                self.read_object,
                self.key_path,
                self.change_list,
            )
            self.widget_container.children = [widgets]
        else:
            self.widget_container.children = [
                v.Html(tag="div", children=["No class selected"])
            ]
