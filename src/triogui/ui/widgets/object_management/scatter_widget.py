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

        self.rebuild_panels()

        self.scatter_container = v.Container(
            children=[self.scatter_panels, self.btn_add_scatter]
        )

        self.content = [self.scatter_container]

    def rebuild_panels(self):
        self.scatter_panels.children = []
        for i, scatter in enumerate(self.scatter_list):
            btn_delete = v.Btn(
                children=[v.Icon(children="mdi-delete")],
                icon=True,
                color="red",
                small=True,
            )
            btn_delete.on_event(
                "click", lambda widget, event, data, idx=i: self.delete_scatter(idx)
            )

            header_content = v.Row(
                children=[
                    v.Col(children=["Scatter"], cols=10),
                    v.Col(children=[btn_delete], cols=2, class_="text-right"),
                ],
                no_gutters=True,
                align="center",
            )

            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[header_content]),
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

    def add_scatter(self, widget, event, data):
        new_scatter = ta.trustify_gen_pyd.Scatter()
        self.scatter_list.append(new_scatter)
        ta.add_read_object(self.dataset, new_scatter)
        self.rebuild_panels()

    def delete_scatter(self, index):
        if 0 <= index < len(self.scatter_list):
            if self.scatter_list[index] is not None:
                ta.delete_read_object(self.dataset, self.scatter_list[index])
            del self.scatter_list[index]

            self.rebuild_panels()
