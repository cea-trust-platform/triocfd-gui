import trioapi as ta
import ipyvuetify as v


class DiscretizeWidget:
    def __init__(self, discretize_list, pb_list, dis_list, dataset):
        self.discretize_list = discretize_list
        self.pb_list = pb_list
        self.dis_list = dis_list
        self.dataset = dataset

        self.discretize_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )
        self.btn_add_discretize = v.Btn(children="Add a discretization")
        self.btn_add_discretize.on_event("click", self.add_discretize)

        self.rebuild_panels()

        self.discretize_container = v.Container(
            children=[self.discretize_panels, self.btn_add_discretize]
        )
        self.content = [self.discretize_container]

    def rebuild_panels(self):
        self.discretize_panels.children = []
        for i, discretize in enumerate(self.discretize_list):
            pb_text_field = v.TextField(
                label="Problem to discretize",
                v_model=discretize[0] if discretize[0] is not None else "",
                placeholder="Enter problem name",
            )

            dis_text_field = v.TextField(
                label="Corresponding scheme",
                v_model=discretize[1] if discretize[1] is not None else "",
                placeholder="Enter discretization scheme",
            )

            btn_delete = v.Btn(
                children=[v.Icon(children="mdi-delete")],
                icon=True,
                color="red",
                small=True,
            )
            btn_delete.on_event(
                "click", lambda widget, event, data, idx=i: self.delete_discretize(idx)
            )

            header_content = v.Row(
                children=[
                    v.Col(children=["Discretization"], cols=10),
                    v.Col(children=[btn_delete], cols=2, class_="text-right"),
                ],
                no_gutters=True,
                align="center",
            )

            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[header_content]),
                    v.ExpansionPanelContent(children=[pb_text_field, dis_text_field]),
                ]
            )
            self.discretize_panels.children = self.discretize_panels.children + [
                new_panel
            ]

            pb_text_field.observe(
                lambda change, idx=i: self.change_discretize_dataset(change, idx, 1),
                "v_model",
            )

            dis_text_field.observe(
                lambda change, idx=i: self.change_discretize_dataset(change, idx, 2),
                "v_model",
            )

    def change_discretize_dataset(self, change, index=None, field_type=None):
        old_item = self.discretize_list[index]
        new_value = change["new"] if change["new"] != "" else None

        if field_type == 1:
            self.discretize_list[index] = [new_value, old_item[1]]
        else:
            self.discretize_list[index] = [old_item[0], new_value]

        if None not in old_item:
            entry_index = ta.get_entry_index(
                self.dataset,
                ta.trustify_gen_pyd.Discretize(
                    problem_name=old_item[0], dis=old_item[1]
                ),
            )
            self.dataset.entries[entry_index] = ta.trustify_gen_pyd.Discretize(
                problem_name=self.discretize_list[index][0],
                dis=self.discretize_list[index][1],
            )
        elif None not in self.discretize_list[index]:
            ta.add_read_object(
                self.dataset,
                ta.trustify_gen_pyd.Discretize(
                    problem_name=self.discretize_list[index][0],
                    dis=self.discretize_list[index][1],
                ),
            )

    def add_discretize(self, widget, event, data):
        self.discretize_list.append([None, None])
        self.rebuild_panels()

    def delete_discretize(self, index):
        if 0 <= index < len(self.discretize_list):
            ta.delete_read_object(
                self.dataset,
                ta.trustify_gen_pyd.Discretize(
                    problem_name=self.discretize_list[index][0],
                    dis=self.discretize_list[index][1],
                ),
            )
            del self.discretize_list[index]

            self.rebuild_panels()
