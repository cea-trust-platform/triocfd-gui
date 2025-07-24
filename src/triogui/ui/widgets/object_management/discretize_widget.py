import trioapi as ta
import ipyvuetify as v


class DiscretizeWidget:
    def __init__(self, discretize_list, dataset):
        """
        Widget definition to manage 'Discretize' entries in the dataset.

        ----------
        Parameters

        discretize_list: list
            A list of [problem_name, discretization_scheme] pairs representing the discretization relations.

        dataset: Dataset
            The dataset being modified by the user.

        This widget provides expansion panels to associate a problem with its discretization scheme.
        Each panel includes two input fields and a delete button.
        """

        # Store internal state
        self.discretize_list = discretize_list
        self.dataset = dataset

        # Button to add a new discretization pair
        self.btn_add_discretize = v.Btn(children="Add a discretization")
        self.btn_add_discretize.on_event("click", self.add_discretize)

        # Create the container for expansion panels
        self.discretize_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        # Build initial UI
        self.rebuild_panels()

        # Container wrapping the UI
        self.discretize_container = v.Container(
            children=[self.discretize_panels, self.btn_add_discretize]
        )
        self.content = [self.discretize_container]

    def rebuild_panels(self):
        """
        Rebuild the list of expansion panels based on the current discretization pairs.
        """

        # Clear existing panels
        self.discretize_panels.children = []

        # Loop through each discretize entry
        for i, discretize in enumerate(self.discretize_list):
            # Text field for the problem name
            pb_text_field = v.TextField(
                label="Problem to discretize",
                v_model=discretize[0] if discretize[0] is not None else "",
                placeholder="Enter problem name",
            )

            # Text field for the discretization scheme
            dis_text_field = v.TextField(
                label="Corresponding scheme",
                v_model=discretize[1] if discretize[1] is not None else "",
                placeholder="Enter discretization scheme",
            )

            # Delete button to remove the entry
            btn_delete = v.Btn(
                children=[v.Icon(children="mdi-delete")],
                icon=True,
                color="red",
                small=True,
            )
            btn_delete.on_event(
                "click", lambda widget, event, data, idx=i: self.delete_discretize(idx)
            )

            # Header layout
            header_content = v.Row(
                children=[
                    v.Col(children=["Discretization"], cols=10),
                    v.Col(children=[btn_delete], cols=2, class_="text-right"),
                ],
                no_gutters=True,
                align="center",
            )

            # Create the expansion panel
            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[header_content]),
                    v.ExpansionPanelContent(children=[pb_text_field, dis_text_field]),
                ]
            )

            # Add the panel to the list
            self.discretize_panels.children = self.discretize_panels.children + [
                new_panel
            ]

            # Observe changes in the problem name field
            pb_text_field.observe(
                lambda change, idx=i: self.change_discretize_dataset(change, idx, 1),
                "v_model",
            )

            # Observe changes in the discretization scheme field
            dis_text_field.observe(
                lambda change, idx=i: self.change_discretize_dataset(change, idx, 2),
                "v_model",
            )

    def change_discretize_dataset(self, change, index=None, field_type=None):
        """
        Called when one of the fields in a discretization pair is modified.

        Updates the internal list and applies the change to the dataset.
        """
        old_item = self.discretize_list[index]
        new_value = change["new"] if change["new"] != "" else None

        # Update the appropriate field
        if field_type == 1:
            self.discretize_list[index] = [new_value, old_item[1]]
        else:
            self.discretize_list[index] = [old_item[0], new_value]

        # If the original entry was complete, update it in the dataset
        if None not in old_item:
            entry_index = ta.get_entry_index(
                self.dataset,
                ta.trustify_gen_pyd.Discretize(
                    problem_name=old_item[0],
                    dis=old_item[1],
                ),
            )
            self.dataset.entries[entry_index] = ta.trustify_gen_pyd.Discretize(
                problem_name=self.discretize_list[index][0],
                dis=self.discretize_list[index][1],
            )

        # If the new entry is now complete, add it to the dataset
        elif None not in self.discretize_list[index]:
            ta.add_read_object(
                self.dataset,
                ta.trustify_gen_pyd.Discretize(
                    problem_name=self.discretize_list[index][0],
                    dis=self.discretize_list[index][1],
                ),
            )

    def add_discretize(self, widget, event, data):
        """
        Add a new empty discretization entry and refresh the UI.
        """
        self.discretize_list.append([None, None])
        self.rebuild_panels()

    def delete_discretize(self, index):
        """
        Delete a discretization entry from both the internal list and the dataset.
        """
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
