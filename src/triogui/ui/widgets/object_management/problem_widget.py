import ipyvuetify as v
import trioapi as ta


class ProblemWidget:
    def __init__(self, pb_list, callback, dataset):
        """
        Widget definition to manage problem object for the dataset

        ----------
        Parameters

        pb_list: list
            Every problem of the dataset


        This widget is composed by a switch
        """

        self.callback = callback
        self.pb_list = pb_list
        self.dataset = dataset

        self.pb_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        self.select_pb = v.Select(
            items=[
                str(i.__name__)
                for i in ta.get_subclass(ta.trustify_gen_pyd.Pb_base.__name__)
            ],
            label="Type of the problem",
            v_model=None,
        )

        self.btn_add_pb = v.Btn(children="Add a problem")
        self.btn_add_pb.on_event("click", self.add_pb)
        for i, pb in enumerate(self.pb_list):
            new_name_pb = v.TextField(
                label="Name of the problem",
                outlined=True,
                v_model=pb[0],
            )
            new_select_pb = v.Select(
                items=[
                    str(i.__name__)
                    for i in ta.get_subclass(ta.trustify_gen_pyd.Pb_base.__name__)
                ],
                label="Type of the problem",
                v_model=type(pb[1]).__name__,
            )

            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Problem"]),
                    v.ExpansionPanelContent(children=[new_name_pb, new_select_pb]),
                ]
            )

            self.pb_panels.children = self.pb_panels.children + [new_panel]
            new_name_pb.observe(
                lambda change, idx=i, name=new_name_pb: self.update_menu(
                    change, idx, name, new_select_pb
                ),
                "v_model",
            )
            new_select_pb.observe(
                lambda change, idx=i, select=new_select_pb: self.update_menu(
                    change, idx, new_name_pb, select
                ),
                "v_model",
            )

        self.pb_container = v.Container(children=[self.pb_panels, self.btn_add_pb])

        self.content = [self.pb_container]

    def update_menu(self, change, index, name_widget, select_widget):
        if change:
            old_item = self.pb_list[index]
            already_created = None not in old_item
            if change["owner"] is name_widget:
                self.pb_list[index] = [change["new"], old_item[1]]
                self.callback(index, 0, already_created, old_item[0], self.dataset)
            else:
                if old_item[1] is not None:
                    new_obj = ta.change_type_object(old_item[1], change["new"])
                else:
                    new_obj = getattr(ta.trustify_gen_pyd, change["new"])()
                self.pb_list[index] = [old_item[0], new_obj]
                self.callback(index, 1, already_created, old_item[0], self.dataset)

    def add_pb(self, widget, event, data):
        index = len(self.pb_list)
        self.pb_list.append([None, None])
        new_name_pb = v.TextField(
            label="Name of the problem",
            outlined=True,
            v_model=None,
        )
        new_select_pb = v.Select(
            items=[
                str(i.__name__)
                for i in ta.get_subclass(ta.trustify_gen_pyd.Pb_base.__name__)
            ],
            label="Type of the problem",
            v_model=None,
        )

        new_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Problem"]),
                v.ExpansionPanelContent(children=[new_name_pb, new_select_pb]),
            ]
        )
        self.pb_panels.children = self.pb_panels.children + [new_panel]

        self.update_menu(None, index, new_name_pb, new_select_pb)
        new_name_pb.observe(
            lambda change, idx=index, name=new_name_pb: self.update_menu(
                change, idx, name, new_select_pb
            ),
            "v_model",
        )
        new_select_pb.observe(
            lambda change, idx=index, select=new_select_pb: self.update_menu(
                change, idx, new_name_pb, select
            ),
            "v_model",
        )
