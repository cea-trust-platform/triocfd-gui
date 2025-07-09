import ipyvuetify as v
import trioapi as ta


class DiscretizationWidget:
    def __init__(self, dis_list):
        """
        Widget definition to manage list object for the dataset

        ----------
        Parameters

        dis_list: list
            Every discretization of the dataset


        """

        self.dis_list = dis_list

        self.dis_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        self.select_dis = v.Select(
            items=[
                str(i.__name__)
                for i in ta.get_subclass(
                    ta.trustify_gen_pyd.Discretisation_base.__name__
                )
            ],
            label="Type of the discretization",
            v_model=None,
        )

        self.btn_add_dis = v.Btn(children="Add a discretization")
        self.btn_add_dis.on_event("click", self.add_dis)
        for dis in self.dis_list:
            new_name_dis = v.TextField(
                label="Name of the discretization",
                outlined=True,
                v_model=dis[0],
            )
            new_select_dis = v.Select(
                items=[
                    str(i.__name__)
                    for i in ta.get_subclass(
                        ta.trustify_gen_pyd.Discretisation_base.__name__
                    )
                ],
                label="Type of the discretization",
                v_model=dis[1].__name__,
            )

            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Discretization"]),
                    v.ExpansionPanelContent(children=[new_name_dis, new_select_dis]),
                ]
            )

            self.dis_panels.children = self.dis_panels.children + [new_panel]

        self.dis_container = v.Container(children=[self.dis_panels, self.btn_add_dis])

        self.content = [self.dis_container]

    def add_dis(self, widget, event, data):
        new_name_dis = v.TextField(
            label="Name of the discretization",
            outlined=True,
            v_model=None,
        )
        new_select_dis = v.Select(
            items=[
                str(i.__name__)
                for i in ta.get_subclass(
                    ta.trustify_gen_pyd.Discretisation_base.__name__
                )
            ],
            label="Type of the discretization",
            v_model=None,
        )

        new_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Discretization"]),
                v.ExpansionPanelContent(children=[new_name_dis, new_select_dis]),
            ]
        )
        self.dis_panels.children = self.dis_panels.children + [new_panel]

        # def update_menu(change):
        #    if change:
        #        old_item = self.dis_list[index]
        #        already_created=(None not in old_item)
        #        if change['owner'] is new_name_dis:
        #            self.dis_list[index] = [change['new'], old_item[1]]
        #            self.dis_callback(index, 0, already_created)
        #        else:
        #            self.dis_list[index] = [old_item[0], getattr(ta.trustify_gen_pyd,change['new'])()]
        #            self.dis_callback(index, 1, already_created)
        # update_menu(None)
        # new_name_dis.observe(update_menu,"v_model")
        # new_select_dis.observe(update_menu,"v_model")
