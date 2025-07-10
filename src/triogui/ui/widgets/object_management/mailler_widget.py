import ipyvuetify as v
import trioapi as ta
from ..object import ObjectWidget


class MaillerWidget:
    def __init__(self, mailler_list, dataset):
        """
        Widget definition to manage list object for the dataset

        ----------
        Parameters

        mailler_list: list
            Every mailler of the dataset


        """

        self.mailler_list = mailler_list
        self.dataset = dataset

        self.mailler_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        self.btn_add_mailler = v.Btn(children="Add a maille")
        self.btn_add_mailler.on_event("click", self.add_mailler)
        for mailler in self.mailler_list:
            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Mailler"]),
                    v.ExpansionPanelContent(
                        children=[
                            ObjectWidget.show_widget(
                                mailler,
                                (ta.trustify_gen_pyd.Mailler, False),
                                mailler,
                                [],
                                [],
                            )
                        ]
                    ),
                ]
            )

            self.mailler_panels.children = self.mailler_panels.children + [new_panel]

        self.mailler_container = v.Container(
            children=[self.mailler_panels, self.btn_add_mailler]
        )

        self.content = [self.mailler_container]

    def add_mailler(self, widget, event, data):
        new_maille = ta.trustify_gen_pyd.Mailler()
        ta.add_read_object(self.dataset, new_maille)
        new_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Mailler"]),
                v.ExpansionPanelContent(
                    children=[
                        ObjectWidget.show_widget(
                            new_maille,
                            (ta.trustify_gen_pyd.Mailler, False),
                            new_maille,
                            [],
                            [],
                        )
                    ]
                ),
            ]
        )

        self.mailler_panels.children = self.mailler_panels.children + [new_panel]
