import ipyvuetify as v
import trioapi as ta
from ..object import ObjectWidget


class MaillerWidget:
    def __init__(self, mailler_list):
        """
        Widget definition to manage list object for the dataset

        ----------
        Parameters

        mailler_list: list
            Every mailler of the dataset


        """

        self.mailler_list = mailler_list

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
        new_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Mailler"]),
                v.ExpansionPanelContent(
                    children=[
                        ObjectWidget.show_widget(
                            None, (ta.trustify_gen_pyd.Mailler, False), None, [], []
                        )
                    ]
                ),
            ]
        )

        self.mailler_panels.children = self.mailler_panels.children + [new_panel]
        # def update_menu(change):
        #    if change:
        #        old_item = self.mailler_list[index]
        #        already_created=(None not in old_item)
        #        if change['owner'] is new_name_mailler:
        #            self.mailler_list[index] = [change['new'], old_item[1]]
        #            self.mailler_callback(index, 0, already_created)
        #        else:
        #            self.mailler_list[index] = [old_item[0], getattr(ta.trustify_gen_pyd,change['new'])()]
        #            self.mailler_callback(index, 1, already_created)
        # update_menu(None)
        # new_name_mailler.observe(update_menu,"v_model")
        # new_select_mailler.observe(update_menu,"v_model")
