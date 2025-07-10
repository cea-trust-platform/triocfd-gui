import ipyvuetify as v
import trioapi as ta
from ..object import ObjectWidget


class ScatterWidget:
    def __init__(self, scatter_list, dataset):
        """
        Widget definition to manage list object for the dataset

        ----------
        Parameters

        scatter_list: list
            Every scatter of the dataset


        """

        self.scatter_list = scatter_list
        self.dataset = dataset

        self.scatter_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        self.btn_add_scatter = v.Btn(children="Add a scatter")
        self.btn_add_scatter.on_event("click", self.add_scatter)
        for scatter in self.scatter_list:
            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Scatter"]),
                    v.ExpansionPanelContent(
                        children=[
                            ObjectWidget.show_widget(
                                scatter,
                                (ta.trustify_gen_pyd.Scatter, False),
                                scatter,
                                [],
                                [],
                            )
                        ]
                    ),
                ]
            )

            self.scatter_panels.children = self.scatter_panels.children + [new_panel]

        self.scatter_container = v.Container(
            children=[self.scatter_panels, self.btn_add_scatter]
        )

        self.content = [self.scatter_container]

    def add_scatter(self, widget, event, data):
        new_scatter = ta.trustify_gen_pyd.Scatter()
        ta.add_read_object(self.dataset, new_scatter)
        new_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Scatter"]),
                v.ExpansionPanelContent(
                    children=[
                        ObjectWidget.show_widget(
                            new_scatter,
                            (ta.trustify_gen_pyd.Scatter, False),
                            new_scatter,
                            [],
                            [],
                        )
                    ]
                ),
            ]
        )

        self.scatter_panels.children = self.scatter_panels.children + [new_panel]
