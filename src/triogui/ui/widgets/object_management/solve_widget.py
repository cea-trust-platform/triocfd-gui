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

        self.rebuild_panels()

        self.solve_container = v.Container(children=[self.solve_panels])

        self.content = [self.solve_container]

    def rebuild_panels(self):
        self.solve_panels.children = []
        for pb in self.pb_list:
            if None not in pb:
                switch = v.Switch(
                    label="Solve this problem", v_model=pb[0] in self.solve_list
                )

                switch.pb_name = pb[0]

                switch.on_event("change", self.change_solve_dataset)

                new_panel = v.ExpansionPanel(
                    children=[
                        v.ExpansionPanelHeader(children=[pb[0]]),
                        v.ExpansionPanelContent(children=[switch]),
                    ]
                )
                self.solve_panels.children = self.solve_panels.children + [new_panel]

    def change_solve_dataset(self, widget, event, data):
        new_value = widget.v_model
        identifier = widget.pb_name
        if new_value:
            ta.solve_problem(self.dataset, identifier)
        else:
            ta.delete_read_object(
                self.dataset, ta.trustify_gen_pyd.Solve(pb=identifier)
            )
            self.solve_list.remove(identifier)
