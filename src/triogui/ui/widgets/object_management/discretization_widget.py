import ipyvuetify as v
import trioapi as ta


class DiscretizationWidget:
    def __init__(self, dis_list, dataset):
        """
        Widget definition to manage list object for the dataset

        ----------
        Parameters

        dis_list: list
            Every discretization of the dataset


        """

        self.dis_list = dis_list
        self.dataset = dataset

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
        for i, dis in enumerate(self.dis_list):
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

            new_name_dis.observe(
                lambda change, idx=i, name=new_name_dis: self.update_dataset(
                    change, idx, name, new_select_dis
                ),
                "v_model",
            )
            new_select_dis.observe(
                lambda change, idx=i, select=new_select_dis: self.update_dataset(
                    change, idx, new_name_dis, select
                ),
                "v_model",
            )

        self.dis_container = v.Container(children=[self.dis_panels, self.btn_add_dis])

        self.content = [self.dis_container]

    def update_dataset(self, change, index, name_widget, select_widget):
        if change:
            old_item = self.dis_list[index]
            already_created = None not in old_item
            if already_created:
                if change["owner"] is name_widget:
                    self.dis_list[index] = [change["new"], old_item[1]]
                    ta.change_declaration_object(
                        self.dataset, old_item[0], "identifier", self.dis_list[index][0]
                    )
                else:
                    new_type = getattr(ta.trustify_gen_pyd, change["new"])
                    self.dis_list[index] = [old_item[0], new_type]
                    ta.change_declaration_object(
                        self.dataset, old_item[0], "ze_type", self.dis_list[index][1]
                    )
            else:
                if change["owner"] is name_widget:
                    self.dis_list[index] = [change["new"], old_item[1]]
                else:
                    new_type = getattr(ta.trustify_gen_pyd, change["new"])
                    self.dis_list[index] = [old_item[0], new_type]
                if None not in self.dis_list[index]:
                    ta.add_declaration_object(
                        self.dataset, self.dis_list[index][1](), self.dis_list[index][0]
                    )

    def add_dis(self, widget, event, data):
        index = len(self.dis_list)
        self.dis_list.append([None, None])
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

        self.update_dataset(None, index, new_name_dis, new_select_dis)
        new_name_dis.observe(
            lambda change, idx=index, name=new_name_dis: self.update_dataset(
                change, idx, name, new_select_dis
            ),
            "v_model",
        )
        new_select_dis.observe(
            lambda change, idx=index, select=new_select_dis: self.update_dataset(
                change, idx, new_name_dis, select
            ),
            "v_model",
        )
