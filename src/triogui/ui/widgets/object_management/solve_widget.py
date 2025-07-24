import trioapi as ta
import ipyvuetify as v


class SolveWidget:
    def __init__(self, solve_list, dataset):
        """
        Widget to manage the list of problems to solve in the dataset.

        Parameters
        ----------

        solve_list: list
            List of problem names currently selected to be solved.

        dataset: Dataset
            The dataset being modified by the user.

        This widget provides an interface to add, and remove problems to solve in the dataset.
        """
        self.solve_list = solve_list
        self.dataset = dataset

        # UI: expansion panels for each solve entry
        self.solve_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        # Button to add a new solve entry
        self.btn_add_solve = v.Btn(children="Add a problem to solve")
        self.btn_add_solve.on_event("click", self.add_solve)

        self.rebuild_panels()

        # Container holding the solve panels and add button
        self.solve_container = v.Container(
            children=[self.solve_panels, self.btn_add_solve]
        )
        self.content = [self.solve_container]

    def rebuild_panels(self):
        """
        Rebuilds the expansion panels based on the current solve_list.
        """
        self.solve_panels.children = []

        for i, solve_item in enumerate(self.solve_list):
            # Text input for problem name to solve
            text_field = v.TextField(
                label="Problem to solve",
                v_model=solve_item if solve_item is not None else "",
                placeholder="Enter problem name to solve",
            )

            # Delete button for each solve entry
            btn_delete = v.Btn(
                children=[v.Icon(children="mdi-delete")],
                icon=True,
                color="red",
                small=True,
            )
            btn_delete.on_event(
                "click", lambda widget, event, data, idx=i: self.delete_solve(idx)
            )

            # Panel header with label and delete button
            header_content = v.Row(
                children=[
                    v.Col(children=["Solve Problem"], cols=10),
                    v.Col(children=[btn_delete], cols=2, class_="text-right"),
                ],
                no_gutters=True,
                align="center",
            )

            # Create expansion panel with header and text input content
            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[header_content]),
                    v.ExpansionPanelContent(children=[text_field]),
                ]
            )

            self.solve_panels.children = self.solve_panels.children + [new_panel]

            # Observe changes in the text field to update solve_list and dataset
            text_field.observe(
                lambda change, idx=i: self.change_solve_dataset(change, idx),
                "v_model",
            )

    def change_solve_dataset(self, change, index=None):
        """
        Updates the solved problems list and the dataset when the name is changed by the user.
        """
        old_item = self.solve_list[index]
        new_value = change.get("new") if change.get("new") != "" else None

        if old_item is not None:
            # Remove previous solve object from dataset
            ta.delete_read_object(self.dataset, ta.trustify_gen_pyd.Solve(pb=old_item))

        # Update solve list with new problem name or None
        self.solve_list[index] = new_value

        if new_value is not None:
            # Add solve object to dataset
            ta.solve_problem(self.dataset, new_value)

    def add_solve(self, widget, event, data):
        """
        Adds a new empty problem solve entry.
        """
        self.solve_list.append(None)
        self.rebuild_panels()

    def delete_solve(self, index):
        """
        Deletes the problem solve entry at the given index and updates dataset.
        """
        if 0 <= index < len(self.solve_list):
            if self.solve_list[index] is not None:
                ta.delete_read_object(
                    self.dataset, ta.trustify_gen_pyd.Solve(pb=self.solve_list[index])
                )
            del self.solve_list[index]
            self.rebuild_panels()
