import ipyvuetify as v
import trioapi as ta


class CoupledProblemWidget:
    def __init__(self, coupled_problem_list, dataset):
        """
        Widget definition to manage a list of coupled problem elements in the dataset.

        ----------
        Parameters

        coupled_problem_list: list
            The list of coupled problem identifiers associated with the dataset.

        dataset: Dataset
            The dataset being modified by the user.

        This widget provides an interface to view, edit, add, or delete a coupled problem element.
        Each problem is represented inside an expansion panel with a text field for editing its name,
        and a delete button.
        """

        # Initialize internal references
        self.coupled_problem_list = coupled_problem_list
        self.dataset = dataset

        # Define the "Add" button
        self.btn_add_coupled_problem = v.Btn(children="Add a coupled problem")
        self.btn_add_coupled_problem.on_event("click", self.add_coupled_problem)

        # Define expansion panels container
        self.coupled_problem_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        # Build the UI from the initial list
        self.rebuild_panels()

        # Compose main container
        self.coupled_problem_container = v.Container(
            children=[self.coupled_problem_panels, self.btn_add_coupled_problem]
        )

        # Store UI elements for rendering
        self.content = [self.coupled_problem_container]

    def rebuild_panels(self):
        """
        Refresh the list of panels based on the current list of coupled problem identifiers.
        """

        # Clear existing panels
        self.coupled_problem_panels.children = []

        # Loop through each problem and build a corresponding panel
        for i, coupled_problem in enumerate(self.coupled_problem_list):
            # Text field to edit the identifier
            new_name_coupled_problem = v.TextField(
                label="Name of the coupled problem",
                outlined=True,
                v_model=coupled_problem,
            )

            # Delete button with trash icon
            btn_delete = v.Btn(
                children=[v.Icon(children="mdi-delete")],
                icon=True,
                color="red",
                small=True,
            )
            # Connect delete action to the button
            btn_delete.on_event(
                "click",
                lambda widget, event, data, idx=i: self.delete_coupled_problem(idx),
            )

            # Header layout with title and delete button
            header_content = v.Row(
                children=[
                    v.Col(children=["Coupled problem"], cols=10),
                    v.Col(children=[btn_delete], cols=2, class_="text-right"),
                ],
                no_gutters=True,
                align="center",
            )

            # Assemble the expansion panel
            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[header_content]),
                    v.ExpansionPanelContent(children=[new_name_coupled_problem]),
                ]
            )

            # Add the new panel to the list
            self.coupled_problem_panels.children = (
                self.coupled_problem_panels.children + [new_panel]
            )

            # Observe changes in the text field to update the dataset accordingly
            new_name_coupled_problem.observe(
                lambda change, idx=i: self.update_dataset(change, idx),
                "v_model",
            )

    def update_dataset(self, change, index):
        """
        Called when a coupled problem name is edited.

        Updates the internal list and modifies the dataset accordingly.
        """
        if change:
            old_identifier = self.coupled_problem_list[index]
            self.coupled_problem_list[index] = change["new"]

            already_created = old_identifier is not None

            # If this problem already exists, update its identifier
            if already_created:
                ta.change_declaration_object(
                    self.dataset,
                    old_identifier,
                    "identifier",
                    self.coupled_problem_list[index],
                )
            # If this is a new problem, add it to the dataset
            else:
                ta.add_declaration_object(
                    self.dataset,
                    ta.trustify_gen_pyd.Coupled_problem(),
                    self.coupled_problem_list[index],
                )

    def add_coupled_problem(self, widget, event, data):
        """
        Add a new (empty) coupled problem entry and refresh the UI.
        """
        self.coupled_problem_list.append(None)
        self.rebuild_panels()

    def delete_coupled_problem(self, index):
        """
        Delete a coupled problem entry by index and update the UI and dataset.
        """
        if 0 <= index < len(self.coupled_problem_list):
            if self.coupled_problem_list[index] in self.dataset._declarations:
                # Remove from dataset if it exists
                ta.delete_declaration_object(
                    self.dataset, self.coupled_problem_list[index]
                )
            # Remove from internal list and refresh
            del self.coupled_problem_list[index]
            self.rebuild_panels()
