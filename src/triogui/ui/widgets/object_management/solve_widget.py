import trioapi as ta
import ipyvuetify as v


class SolveWidget:
    def __init__(self, pb_list, solve_list, dataset):
        self.pb_list = pb_list
        self.solve_list = solve_list
        self.dataset = dataset

        self.solve_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )
        self.btn_add_solve = v.Btn(children="Add a problem to solve")
        self.btn_add_solve.on_event("click", self.add_solve)

        self.rebuild_panels()

        self.solve_container = v.Container(
            children=[self.solve_panels, self.btn_add_solve]
        )
        self.content = [self.solve_container]

    def rebuild_panels(self):
        self.solve_panels.children = []
        for i, solve_item in enumerate(self.solve_list):
            text_field = v.TextField(
                label="Problem to solve",
                v_model=solve_item if solve_item is not None else "",
                placeholder="Enter problem name to solve",
            )

            btn_delete = v.Btn(
                children=[v.Icon(children="mdi-delete")],
                icon=True,
                color="red",
                small=True,
            )
            btn_delete.on_event(
                "click", lambda widget, event, data, idx=i: self.delete_solve(idx)
            )

            header_content = v.Row(
                children=[
                    v.Col(children=["Solve Problem"], cols=10),
                    v.Col(children=[btn_delete], cols=2, class_="text-right"),
                ],
                no_gutters=True,
                align="center",
            )

            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[header_content]),
                    v.ExpansionPanelContent(children=[text_field]),
                ]
            )
            self.solve_panels.children = self.solve_panels.children + [new_panel]

            text_field.observe(
                lambda change, idx=i: self.change_solve_dataset(change, idx),
                "v_model",
            )

    def change_solve_dataset(self, change, index=None):
        old_item = self.solve_list[index]
        new_value = change["new"] if change["new"] != "" else None

        if old_item is not None:
            ta.delete_read_object(self.dataset, ta.trustify_gen_pyd.Solve(pb=old_item))

        self.solve_list[index] = new_value

        if new_value is not None:
            ta.solve_problem(self.dataset, new_value)

    def add_solve(self, widget, event, data):
        self.solve_list.append(None)
        self.rebuild_panels()

    def delete_solve(self, index):
        if 0 <= index < len(self.solve_list):
            if self.solve_list[index] is not None:
                ta.delete_read_object(
                    self.dataset, ta.trustify_gen_pyd.Solve(pb=self.solve_list[index])
                )
            del self.solve_list[index]
            self.rebuild_panels()
