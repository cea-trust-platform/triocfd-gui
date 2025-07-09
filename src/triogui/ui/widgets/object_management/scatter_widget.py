import ipyvuetify as v
import trioapi as ta
from ..object import ObjectWidget


class ScatterWidget:
    def __init__(self, scatter_list):
        """
        Widget definition to manage list object for the dataset

        ----------
        Parameters

        scatter_list: list
            Every scatter of the dataset


        """

        self.scatter_list = scatter_list

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
        new_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Scatter"]),
                v.ExpansionPanelContent(
                    children=[
                        ObjectWidget.show_widget(
                            None, (ta.trustify_gen_pyd.Scatter, False), None, [], []
                        )
                    ]
                ),
            ]
        )

        self.scatter_panels.children = self.scatter_panels.children + [new_panel]
        # def update_menu(change):
        #    if change:
        #        old_item = self.scatter_list[index]
        #        already_created=(None not in old_item)
        #        if change['owner'] is new_name_scatter:
        #            self.scatter_list[index] = [change['new'], old_item[1]]
        #            self.scatter_callback(index, 0, already_created)
        #        else:
        #            self.scatter_list[index] = [old_item[0], getattr(ta.trustify_gen_pyd,change['new'])()]
        #            self.scatter_callback(index, 1, already_created)
        # update_menu(None)
        # new_name_scatter.observe(update_menu,"v_model")
        # new_select_scatter.observe(update_menu,"v_model")
