import ipyvuetify as v
import trioapi as ta


class SchemeWidget:
    def __init__(self, sch_list, sch_callback, ds_callback, dataset):
        """
        Widget to manage schemes of the dataset.

        ----------
        Parameters

        sch_list: list
            List of scheme tuples. Each item is [name: str, instance: Schema_temps_base].

        sch_callback: function
            Callback triggered when a scheme is renamed or its type is changed.

        ds_callback: function
            Callback triggered when the dataset changes.

        dataset: Dataset
            The dataset being modified by the user.

        This widget provides an interface to add, edit (type and name), and remove schemes from the dataset.
        """

        self.sch_list = sch_list
        self.sch_callback = sch_callback
        self.ds_callback = ds_callback
        self.dataset = dataset

        # UI: expansion panels for each scheme
        self.sch_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        # Build list of available scheme types and their docstrings
        self.sch_with_doc = []
        self.doc_dict = {}
        for sch in ta.get_subclass("Schema_temps_base"):
            sch_name = sch.__name__
            sch_doc = sch.__doc__
            self.sch_with_doc.append(
                {"text": f"{sch_name} - {sch_doc}", "value": sch_name}
            )
            self.doc_dict[sch_name] = sch_doc

        # Button to add a new scheme
        self.btn_add_sch = v.Btn(children="Add a scheme")
        self.btn_add_sch.on_event("click", self.add_sch)

        self.rebuild_panels()

        # Final container holding all UI components
        self.sch_container = v.Container(children=[self.sch_panels, self.btn_add_sch])
        self.content = [self.sch_container]

    def rebuild_panels(self):
        """
        Clears and rebuilds the expansion panels for each scheme in the list.
        """
        self.sch_panels.children = []

        for i, sch in enumerate(self.sch_list):
            # Input for scheme name
            new_name_sch = v.TextField(
                label="Name of the scheme",
                outlined=True,
                v_model=sch[0],
            )

            # Dropdown for selecting scheme type
            new_select_sch = v.Select(
                items=self.sch_with_doc,
                label="Type of the scheme",
                v_model=type(sch[1]).__name__,
            )

            # Documentation viewer
            doc_display = v.Alert(
                children=["Select an element to see its documentation"]
                if sch[1] is None
                else [self.doc_dict.get(new_select_sch.v_model)],
                type="info",
                outlined=True,
                class_="text-body-2 pa-2 mt-2",
                style_="white-space: pre-wrap;",
            )

            # Delete button
            btn_delete = v.Btn(
                children=[v.Icon(children="mdi-delete")],
                icon=True,
                color="red",
                small=True,
            )
            btn_delete.on_event(
                "click", lambda widget, event, data, idx=i: self.delete_sch(idx)
            )

            # Panel header row
            header_content = v.Row(
                children=[
                    v.Col(children=["Scheme"], cols=10),
                    v.Col(children=[btn_delete], cols=2, class_="text-right"),
                ],
                no_gutters=True,
                align="center",
            )

            # Full panel with header and form content
            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[header_content]),
                    v.ExpansionPanelContent(
                        children=[
                            new_name_sch,
                            new_select_sch,
                            doc_display,
                        ]
                    ),
                ]
            )

            self.sch_panels.children = self.sch_panels.children + [new_panel]

            # Observe name and type changes
            new_name_sch.observe(
                lambda change, idx=i, name=new_name_sch: self.update_menu(
                    change, idx, name, new_select_sch
                ),
                "v_model",
            )
            new_select_sch.observe(
                lambda change, idx=i, select=new_select_sch: self.update_menu(
                    change, idx, new_name_sch, select
                ),
                "v_model",
            )
            new_select_sch.observe(
                lambda change, display=doc_display: self.update_doc(change, display),
                "v_model",
            )

    def update_doc(self, change, display_widget):
        """
        Updates the documentation alert box when a scheme type is selected.
        """
        if change and change.get("new"):
            selected_value = change["new"]
            doc_text = self.doc_dict.get(selected_value)
            display_widget.children = [doc_text]

    def update_menu(self, change, index, name_widget, select_widget):
        """
        Updates the scheme list and the dataset when the name or type is changed by the user.
        """
        if change:
            old_item = self.sch_list[index]
            already_created = None not in old_item

            if change["owner"] is name_widget:
                # Name changed
                self.sch_list[index] = [change["new"], old_item[1]]
                self.sch_callback(
                    index, 0, already_created, old_item[0], self.dataset
                )  # Callback to change the menu and the dataset
            else:
                # Type changed
                if old_item[1] is not None:
                    new_obj = ta.change_type_object(old_item[1], change["new"])
                else:
                    new_obj = getattr(ta.trustify_gen_pyd, change["new"])()
                self.sch_list[index] = [old_item[0], new_obj]
                self.sch_callback(
                    index, 1, already_created, old_item[0], self.dataset
                )  # Callback to change the menu and the dataset

    def add_sch(self, widget, event, data):
        """
        Adds a new empty scheme entry.
        """
        self.sch_list.append([None, None])
        self.rebuild_panels()

    def delete_sch(self, index):
        """
        Deletes a scheme from the list and updates the dataset.
        """
        if 0 <= index < len(self.sch_list):
            if self.sch_list[index][0] in self.dataset._declarations:
                ta.delete_object(self.dataset, self.sch_list[index][0])
            del self.sch_list[index]
            self.ds_callback(self.dataset)  # Callback to update the menu of the app
            self.rebuild_panels()
