import ipyvuetify as v
import trioapi as ta
from ..object import ObjectWidget


class DiscretizationWidget:
    def __init__(self, dis_list, dataset):
        """
        Widget definition to manage discretizations in the dataset.

        ----------
        Parameters

        dis_list: list
            A list of discretizations, where each element is a list [identifier, type].

        dataset: Dataset
            The dataset being modified by the user.

        This widget displays a list of discretizations using expansion panels.
        Each panel contains a text field for the name, a dropdown to select the type,
        and an information alert displaying the documentation of the selected type.
        """

        # Save references
        self.dis_list = dis_list
        self.dataset = dataset

        # Prepare available discretization types with their documentation
        self.dis_with_doc = []
        self.doc_dict = {}
        for dis in ta.get_subclass("Discretisation_base"):
            dis_name = dis.__name__
            dis_doc = dis.__doc__
            self.dis_with_doc.append(
                {"text": f"{dis_name} - {dis_doc}", "value": dis_name}
            )
            self.doc_dict[dis_name] = dis_doc

        # Create the expansion panel container
        self.dis_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        # Add button to insert a new discretization
        self.btn_add_dis = v.Btn(children="Add a discretization")
        self.btn_add_dis.on_event("click", self.add_dis)

        # Build initial UI from existing data
        self.rebuild_panels()

        # Wrap the UI in a container
        self.dis_container = v.Container(children=[self.dis_panels, self.btn_add_dis])
        self.content = [self.dis_container]

    def rebuild_panels(self):
        """
        Refresh the list of expansion panels from the current discretization list.
        """

        # Clear the panel list
        self.dis_panels.children = []

        # Build each panel
        for i, dis in enumerate(self.dis_list):
            # Text field for the discretization name
            new_name_dis = v.TextField(
                label="Name of the discretization",
                outlined=True,
                v_model=dis[0],
            )

            # Select dropdown for the discretization type
            new_select_dis = v.Select(
                items=self.dis_with_doc,
                label="Type of the discretization",
                v_model=dis[1].__name__ if dis[1] is not None else None,
            )

            # Display the documentation for the selected type
            doc_display = v.Alert(
                children=["Select an element to see its documentation"]
                if dis[1] is None
                else [self.doc_dict.get(new_select_dis.v_model)],
                type="info",
                outlined=True,
                class_="text-body-2 pa-2 mt-2",
                style_="white-space: pre-wrap;",
            )

            # Delete button to remove this discretization
            btn_delete = v.Btn(
                children=[v.Icon(children="mdi-delete")],
                icon=True,
                color="red",
                small=True,
            )
            btn_delete.on_event(
                "click", lambda widget, event, data, idx=i: self.delete_dis(idx)
            )

            # Header row with label and delete button
            header_content = v.Row(
                children=[
                    v.Col(children=["Discretization"], cols=10),
                    v.Col(children=[btn_delete], cols=2, class_="text-right"),
                ],
                no_gutters=True,
                align="center",
            )

            # Container for dynamic content (initially empty)
            dynamic_content = v.Container(children=[])

            content_children = [
                new_name_dis,
                new_select_dis,
                doc_display,
                dynamic_content,
            ]

            # Compose the panel with header and content
            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[header_content]),
                    v.ExpansionPanelContent(children=content_children),
                ]
            )

            # Verify to update the content if the dis is Vef
            self.update_widget_for_vef(i, dynamic_content)

            # Add the panel to the UI
            self.dis_panels.children = self.dis_panels.children + [new_panel]

            # Observe changes to name field and update dataset
            new_name_dis.observe(
                lambda change,
                idx=i,
                name=new_name_dis,
                content=dynamic_content: self.update_dataset(
                    change, idx, name, new_select_dis, content
                ),
                "v_model",
            )

            # Observe changes to type dropdown and update dataset
            new_select_dis.observe(
                lambda change,
                idx=i,
                select=new_select_dis,
                content=dynamic_content: self.update_dataset(
                    change, idx, new_name_dis, select, content
                ),
                "v_model",
            )

            # Observe changes to dropdown and update documentation view
            new_select_dis.observe(
                lambda change, display=doc_display: self.update_doc(change, display),
                "v_model",
            )

    def update_doc(self, change, display_widget):
        """
        Update the documentation alert with the docstring of the selected discretization type.
        """
        if change and change.get("new"):
            selected_value = change["new"]
            doc_text = self.doc_dict.get(selected_value)
            display_widget.children = [doc_text]

    def update_dataset(
        self, change, index, name_widget, select_widget, widget_container
    ):
        """
        Update the dataset when a name or type field is changed.

        If the entry was already created, it is updated.
        If both fields are filled for a new entry, it is added to the dataset.
        """
        if change:
            old_item = self.dis_list[index]
            already_created = None not in old_item

            # If the discretization already exists, update the appropriate field
            if already_created:
                if change["owner"] is name_widget:
                    # Update identifier
                    self.dis_list[index] = [change["new"], old_item[1]]
                    # We use the appropriate function if the dis is used with the read keyword or not
                    if self.dataset._declarations[old_item[0]][1] == -1:
                        ta.change_declaration_object(
                            self.dataset,
                            old_item[0],
                            "identifier",
                            self.dis_list[index][0],
                        )
                    else:
                        ta.change_read_object(
                            self.dataset,
                            old_item[0],
                            "identifier",
                            self.dis_list[index][0],
                        )
                else:
                    # Update type
                    new_type = getattr(ta.trustify_gen_pyd, change["new"])
                    self.dis_list[index] = [old_item[0], new_type]
                    # This if means that the old type was Vef (only dis with read keyword)
                    if self.dataset._declarations[old_item[0]][1] > 0:
                        entry_index = self.dataset._declarations[old_item[0]][1]
                        # Delete in the dataset entries
                        del self.dataset.entries[entry_index]
                        self.dataset._declarations[old_item[0]][1] = -1
                    # Change for the declaration
                    ta.change_declaration_object(
                        self.dataset, old_item[0], "ze_type", self.dis_list[index][1]
                    )
            # If it's a new entry, fill in values and add to dataset if complete
            else:
                if change["owner"] is name_widget:
                    self.dis_list[index] = [change["new"], old_item[1]]
                else:
                    new_type = getattr(ta.trustify_gen_pyd, change["new"])
                    self.dis_list[index] = [old_item[0], new_type]

                if None not in self.dis_list[index]:
                    ta.add_declaration_object(
                        self.dataset,
                        self.dis_list[index][1](),  # Instantiate the type
                        self.dis_list[index][0],
                    )
            # Keep the widget for vef updated
            self.update_widget_for_vef(index, widget_container)

    def update_widget_for_vef(self, index, widget_container):
        """
        Creates a widget specially for the Vef discretization to let the user modifies it if he wants to.
        It is the only discretization with the keyword read available
        """
        # Empty the container
        widget_container.children = []
        if (
            self.dis_list[index][0] is not None
            and self.dis_list[index][1] == ta.trustify_gen_pyd.Vef
        ):
            # Choose to change the discretization or not
            switch = v.Switch(
                label="Modify this discretization using the Read keyword ?",
                v_model=self.dataset._declarations[self.dis_list[index][0]][1] > 0,
            )
            switch.observe(
                lambda change: self.update_read_dis(change, index, widget_container),
                "v_model",
            )
            widget_container.children = widget_container.children + [switch]
            # Create the widget if it is already modified in the dataset
            if self.dataset._declarations[self.dis_list[index][0]][1] > 0:
                widget = ObjectWidget.show_widget(
                    self.dataset.get(self.dis_list[index][0]),
                    (self.dis_list[index][1], False),
                    self.dataset.get(self.dis_list[index][0]),
                    [],
                    [],
                    True,
                )
                widget_container.children = widget_container.children + [widget]

    def add_dis(self, widget, event, data):
        """
        Add a new empty discretization to the list kand refresh the UI.
        """
        self.dis_list.append([None, None])
        self.rebuild_panels()

    def delete_dis(self, index):
        """
        Delete a discretization by index from both the list and the dataset.
        """
        if 0 <= index < len(self.dis_list):
            if self.dis_list[index][0] in self.dataset._declarations:
                # Use the appropriate function depending on if it uses the keyword read or not
                if self.dataset._declarations[self.dis_list[index][0]][1] > 0:
                    ta.delete_object(self.dataset, self.dis_list[index][0])
                else:
                    ta.delete_declaration_object(self.dataset, self.dis_list[index][0])
            del self.dis_list[index]
            self.rebuild_panels()

    def update_read_dis(self, change, index, widget_container):
        """
        Update the database by creating or deleting the Read keyword according to the switch changes.
        """
        if change["new"]:
            # Write the Read keyword and change in the dataset _declarations
            read_dis = ta.trustify_gen_pyd.Read(
                identifier=self.dis_list[index][0], obj=self.dis_list[index][1]()
            )
            ta.add_read_object(self.dataset, read_dis)
            entry_index = ta.get_entry_index(self.dataset, read_dis)
            self.dataset._declarations[self.dis_list[index][0]][1] = entry_index
        else:
            # Delete the Read keyword
            entry_index = self.dataset._declarations[self.dis_list[index][0]][1]
            del self.dataset.entries[entry_index]
            self.dataset._declarations[self.dis_list[index][0]][1] = -1
        # Keep the widget updated
        self.update_widget_for_vef(index, widget_container)
