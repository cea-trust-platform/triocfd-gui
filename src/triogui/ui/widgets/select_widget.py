import ipyvuetify as v
import trioapi as ta
from .object import ObjectWidget


class SelectWidget:
    def __init__(self, initial_type):
        """
        Widget definition for Select Widget

        ----------
        Parameters

        initial_type: pydantic class
            We choose a subclass of this type to create a new object

        This widget is composed by a select to choose the type and then display widget for each attributes of the type
        """

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
        self.content = v.Content(children=[self.select, self.expand_panel])

        # Initial call
        self.change_class(None)

    def change_class(self, event):
        # Cleaning old container
        self.widget_container.children = []

        selected = self.select.v_model
        if selected:
            widgets = ObjectWidget.show_widget(
                ta.get_successive_attributes(ta.trustify_gen_pyd.__dict__[selected]),
                None,
            )
            self.widget_container.children = [widgets]
        else:
            self.widget_container.children = [
                v.Html(tag="div", children=["No class selected"])
            ]
