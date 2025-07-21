import ipyvuetify as v
import trioapi as ta


class CoupledProblemWidget:
    def __init__(self, coupled_problem_list, dataset):
        """
        Widget definition to manage list object for the dataset

        ----------
        Parameters

        coupled_problem_list: list
            Every coupled_problememe of the dataset
        """

        self.coupled_problem_list = coupled_problem_list
        self.dataset = dataset

        self.coupled_problem_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        self.btn_add_coupled_problem = v.Btn(children="Add a coupled problem")
        self.btn_add_coupled_problem.on_event("click", self.add_coupled_problem)
        self.rebuild_panels()

        self.coupled_problem_container = v.Container(
            children=[self.coupled_problem_panels, self.btn_add_coupled_problem]
        )

        self.content = [self.coupled_problem_container]

    def rebuild_panels(self):
        self.coupled_problem_panels.children = []
        for i, coupled_problem in enumerate(self.coupled_problem_list):
            new_name_coupled_problem = v.TextField(
                label="Name of the coupled problem",
                outlined=True,
                v_model=coupled_problem,
            )

            btn_delete = v.Btn(
                children=[v.Icon(children="mdi-delete")],
                icon=True,
                color="red",
                small=True,
            )
            btn_delete.on_event(
                "click",
                lambda widget, event, data, idx=i: self.delete_coupled_problem(idx),
            )

            header_content = v.Row(
                children=[
                    v.Col(children=["Coupled problem"], cols=10),
                    v.Col(children=[btn_delete], cols=2, class_="text-right"),
                ],
                no_gutters=True,
                align="center",
            )

            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[header_content]),
                    v.ExpansionPanelContent(children=[new_name_coupled_problem]),
                ]
            )

            self.coupled_problem_panels.children = (
                self.coupled_problem_panels.children + [new_panel]
            )

            new_name_coupled_problem.observe(
                lambda change, idx=i: self.update_dataset(change, idx),
                "v_model",
            )

    def update_dataset(self, change, index):
        if change:
            old_identifier = self.coupled_problem_list[index]
            self.coupled_problem_list[index] = change["new"]
            already_created = old_identifier is not None
            if already_created:
                ta.change_declaration_object(
                    self.dataset,
                    old_identifier,
                    "identifier",
                    self.coupled_problem_list[index],
                )
            else:
                ta.add_declaration_object(
                    self.dataset,
                    ta.trustify_gen_pyd.Coupled_problem(),
                    self.coupled_problem_list[index],
                )

    def add_coupled_problem(self, widget, event, data):
        self.coupled_problem_list.append(None)
        self.rebuild_panels()

    def delete_coupled_problem(self, index):
        if 0 <= index < len(self.coupled_problem_list):
            if self.coupled_problem_list[index] in self.dataset._declarations:
                ta.delete_declaration_object(
                    self.dataset, self.coupled_problem_list[index]
                )
            del self.coupled_problem_list[index]
            self.rebuild_panels()
