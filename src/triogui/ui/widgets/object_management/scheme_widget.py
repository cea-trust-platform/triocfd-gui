import ipyvuetify as v
import trioapi as ta


class SchemeWidget:
    def __init__(self, sch_list, sch_callback, dataset):
        """
        Widget definition to manage list object for the dataset

        ----------
        Parameters

        sch_list: list
            Every scheme of the dataset
        """

        self.sch_callback = sch_callback
        self.sch_list = sch_list
        self.dataset = dataset

        self.sch_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        self.select_sch = v.Select(
            items=[
                str(i.__name__)
                for i in ta.get_subclass(ta.trustify_gen_pyd.Schema_temps_base.__name__)
            ],
            label="Type of the scheme",
            v_model=None,
        )

        self.btn_add_sch = v.Btn(children="Add a scheme")
        self.btn_add_sch.on_event("click", self.add_sch)
        for i, sch in enumerate(self.sch_list):
            new_name_sch = v.TextField(
                label="Name of the scheme",
                outlined=True,
                v_model=sch[0],
            )
            new_select_sch = v.Select(
                items=[
                    str(i.__name__)
                    for i in ta.get_subclass(
                        ta.trustify_gen_pyd.Schema_temps_base.__name__
                    )
                ],
                label="Type of the scheme",
                v_model=type(sch[1]).__name__,
            )

            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Scheme"]),
                    v.ExpansionPanelContent(children=[new_name_sch, new_select_sch]),
                ]
            )

            self.sch_panels.children = self.sch_panels.children + [new_panel]
            new_name_sch.observe(
                lambda change, idx=i, name=new_name_sch: self.update_menu(
                    change, idx, name, new_select_sch
                ),
                "v_model",
            )
            new_select_sch.observe(
                lambda change, idx=i, select=new_select_sch: self.update_menu(
                    change, idx, new_name_sch, select
                ),
                "v_model",
            )

        self.sch_container = v.Container(children=[self.sch_panels, self.btn_add_sch])

        self.content = [self.sch_container]

    def update_menu(self, change, index, name_widget, select_widget):
        if change:
            old_item = self.sch_list[index]
            already_created = None not in old_item
            if change["owner"] is name_widget:
                self.sch_list[index] = [change["new"], old_item[1]]
                self.sch_callback(index, 0, already_created, old_item[0], self.dataset)
            else:
                if old_item[1] is not None:
                    new_obj = ta.change_type_object(old_item[1], change["new"])
                else:
                    new_obj = getattr(ta.trustify_gen_pyd, change["new"])()
                self.sch_list[index] = [old_item[0], new_obj]
                self.sch_callback(index, 1, already_created, old_item[0], self.dataset)

    def add_sch(self, widget, event, data):
        index = len(self.sch_list)
        self.sch_list.append([None, None])
        new_name_sch = v.TextField(
            label="Name of the scheme",
            outlined=True,
            v_model=None,
        )
        new_select_sch = v.Select(
            items=[
                str(i.__name__)
                for i in ta.get_subclass(ta.trustify_gen_pyd.Schema_temps_base.__name__)
            ],
            label="Type of the scheme",
            v_model=None,
        )

        new_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Scheme"]),
                v.ExpansionPanelContent(children=[new_name_sch, new_select_sch]),
            ]
        )
        self.sch_panels.children = self.sch_panels.children + [new_panel]

        self.update_menu(None, index, new_name_sch, new_select_sch)
        new_name_sch.observe(
            lambda change, idx=index, name=new_name_sch: self.update_menu(
                change, idx, name, new_select_sch
            ),
            "v_model",
        )
        new_select_sch.observe(
            lambda change, idx=index, select=new_select_sch: self.update_menu(
                change, idx, new_name_sch, select
            ),
            "v_model",
        )
