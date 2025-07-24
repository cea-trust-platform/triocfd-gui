import trioapi as ta
import ipyvuetify as v


class AssociateWidget:
    def __init__(self, associate_list, dataset):
        """
        Widget definition for Association Widget

        ----------
        Parameters

        associate_list: List
            The list of list of two elements which are the identifier of associed elements

        dataset: Dataset
            The dataset which is being modified by the user

        This widget is composed by an expansion panel for each association of the dataset and a button to add an expansion panel.
        Each expansion panel is composed by two textfields to write the identifier of the objects we want to associate.
        """

        # Initialization
        self.associate_list = associate_list
        self.dataset = dataset

        # Definition of the add button
        self.btn_add_associate = v.Btn(children="Add an association")
        self.btn_add_associate.on_event("click", self.add_associate)

        # Define expansion panels container
        self.associate_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )
        # Build the UI from the initial list
        self.rebuild_panels()

        # Compose main container
        self.associate_container = v.Container(
            children=[self.associate_panels, self.btn_add_associate]
        )
        # Store UI elements for rendering
        self.content = [self.associate_container]

    def rebuild_panels(self):
        """
        Refresh the list of panels based on the current list of associed objects identifiers.
        """

        # Reinitiliaze the panel
        self.associate_panels.children = []

        # Loop through each association in the list
        for i, associate in enumerate(self.associate_list):
            # First input field for the first object in the association
            text_field_1 = v.TextField(
                label="First object to associate",
                v_model=associate[0] if associate[0] is not None else "",
                placeholder="Enter first object name",
            )

            # Second input field for the second object in the association
            text_field_2 = v.TextField(
                label="Second object to associate",
                v_model=associate[1] if associate[1] is not None else "",
                placeholder="Enter second object name",
            )

            # Delete button with trash icon
            btn_delete = v.Btn(
                children=[v.Icon(children="mdi-delete")],
                icon=True,
                color="red",
                small=True,
            )
            # On click, delete this association by index
            btn_delete.on_event(
                "click", lambda widget, event, data, idx=i: self.delete_associate(idx)
            )

            # Header content with label and delete button
            header_content = v.Row(
                children=[
                    v.Col(children=["Association"], cols=10),
                    v.Col(children=[btn_delete], cols=2, class_="text-right"),
                ],
                no_gutters=True,
                align="center",
            )

            # Create the expansion panel with header and inputs
            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[header_content]),
                    v.ExpansionPanelContent(children=[text_field_1, text_field_2]),
                ]
            )

            # Add the new panel to the panel list
            self.associate_panels.children = self.associate_panels.children + [
                new_panel
            ]

            # Observe changes to the first text field and update the dataset
            text_field_1.observe(
                lambda change, idx=i: self.change_associate_dataset(change, idx, 1),
                "v_model",
            )

            # Observe changes to the second text field and update the dataset
            text_field_2.observe(
                lambda change, idx=i: self.change_associate_dataset(change, idx, 2),
                "v_model",
            )

    def change_associate_dataset(self, change, index=None, field_type=None):
        """
        Called when an association textfield is changed to change the association list and the associations in the dataset
        """
        old_item = self.associate_list[index]
        new_value = change["new"] if change["new"] != "" else None

        # Update the selected field in the association
        if field_type == 1:
            self.associate_list[index] = [new_value, old_item[1]]
        else:
            self.associate_list[index] = [old_item[0], new_value]

        # If the previous association was complete, update it in the dataset
        if None not in old_item:
            entry_index = ta.get_entry_index(
                self.dataset,
                ta.trustify_gen_pyd.Associate(objet_1=old_item[0], objet_2=old_item[1]),
            )
            self.dataset.entries[entry_index] = ta.trustify_gen_pyd.Associate(
                objet_1=self.associate_list[index][0],
                objet_2=self.associate_list[index][1],
            )
        # If the new association is now complete, add it to the dataset
        elif None not in self.associate_list[index]:
            ta.add_read_object(
                self.dataset,
                ta.trustify_gen_pyd.Associate(
                    objet_1=self.associate_list[index][0],
                    objet_2=self.associate_list[index][1],
                ),
            )

    def add_associate(self, widget, event, data):
        """
        Add a new empty association and refresh the UI
        """
        self.associate_list.append([None, None])
        self.rebuild_panels()

    def delete_associate(self, index):
        """
        Delete an association by index and refresh the UI
        """
        if 0 <= index < len(self.associate_list):
            ta.delete_read_object(
                self.dataset,
                ta.trustify_gen_pyd.Associate(
                    objet_1=self.associate_list[index][0],
                    objet_2=self.associate_list[index][1],
                ),
            )
            del self.associate_list[index]
            self.rebuild_panels()
