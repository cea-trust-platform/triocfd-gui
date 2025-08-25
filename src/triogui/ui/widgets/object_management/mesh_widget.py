import ipyvuetify as v
import trioapi as ta
from ..object import ObjectWidget


class MeshWidget:
    def __init__(self, mesh_list, dataset):
        """
        Widget definition to manage meshes in the dataset.

        ----------
        Parameters

        mesh_list: list
            List of meshes to manage within the dataset.

        dataset: Dataset
            The dataset to which the mesh objects are linked.

        This widget allows interactive creation, selection, and deletion of meshes.
        Mesh classes include Read_med, Read_file, Read_file_bin, and Read_tgrid, each with
        a description shown when selected.
        """

        self.mesh_list = mesh_list
        self.dataset = dataset

        # Create container for all mesh panels
        self.mesh_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        # Available mesh types with docstrings for selection
        self.mesh_available = ["Read_med", "Read_file", "Read_file_bin", "Read_tgrid"]
        self.mesh_with_doc = []
        self.doc_dict = {}

        for mesh in self.mesh_available:
            mesh_class = getattr(ta.trustify_gen_pyd, mesh)
            mesh_name = mesh_class.__name__
            mesh_doc = mesh_class.__doc__
            self.mesh_with_doc.append(
                {"text": f"{mesh_name} - {mesh_doc}", "value": mesh_name}
            )
            self.doc_dict[mesh_name] = mesh_doc

        # Add mesh button
        self.btn_add_mesh = v.Btn(children="Add a mesh")
        self.btn_add_mesh.on_event("click", self.add_mesh)

        self.rebuild_panels()

        self.mesh_container = v.Container(
            children=[self.mesh_panels, self.btn_add_mesh]
        )

        self.content = [self.mesh_container]

    def rebuild_panels(self):
        """
        Rebuilds all mesh expansion panels, including selection dropdown,
        documentation, and mesh-specific fields.
        """
        self.mesh_panels.children = []

        for i, mesh in enumerate(self.mesh_list):
            # Dropdown to select mesh type
            new_select_type_mesh = v.Select(
                items=self.mesh_with_doc,
                label="Type of the mesh",
                v_model=None,
            )

            # Info box to display documentation of the selected mesh type
            doc_display = v.Alert(
                children=["Select an element to see its documentation"],
                type="info",
                outlined=True,
                class_="text-body-2 pa-2 mt-2",
                style_="white-space: pre-wrap;",
            )

            # Pre-fill UI if mesh is already selected
            if mesh is not None:
                mesh_type_name = type(mesh).__name__
                new_select_type_mesh.v_model = mesh_type_name
                doc_display.children = [self.doc_dict.get(mesh_type_name)]
                panel_content = [
                    new_select_type_mesh,
                    doc_display,
                    ObjectWidget.show_widget(
                        mesh, (type(mesh), False), mesh, [], [], True
                    ),
                ]
            else:
                panel_content = [new_select_type_mesh, doc_display]

            # Delete button for the current mesh
            btn_delete = v.Btn(
                children=[v.Icon(children="mdi-delete")],
                icon=True,
                color="red",
                small=True,
            )
            btn_delete.on_event(
                "click", lambda widget, event, data, idx=i: self.delete_mesh(idx)
            )

            header_content = v.Row(
                children=[
                    v.Col(children=["Mesh"], cols=10),
                    v.Col(children=[btn_delete], cols=2, class_="text-right"),
                ],
                no_gutters=True,
                align="center",
            )

            # Create expansion panel for this mesh
            expansion_panel_content = v.ExpansionPanelContent(children=panel_content)
            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[header_content]),
                    expansion_panel_content,
                ]
            )

            # Event listener for mesh type selection to update the panel content
            new_select_type_mesh.observe(
                lambda change,
                idx=i,
                select=new_select_type_mesh,
                content=expansion_panel_content: self.change_class(
                    change, idx, select, content, doc_display
                ),
                "v_model",
            )

            # Event listener for doc update
            new_select_type_mesh.observe(
                lambda change, display=doc_display: self.update_doc(change, display),
                "v_model",
            )

            self.mesh_panels.children = self.mesh_panels.children + [new_panel]

    def update_doc(self, change, display_widget):
        """
        Update the documentation alert box based on selected mesh type.
        """
        if change and change.get("new"):
            selected_value = change["new"]
            doc_text = self.doc_dict.get(selected_value)
            display_widget.children = [doc_text]

    def add_mesh(self, widget, event, data):
        """
        Add a new (empty) mesh entry to the list.
        """
        self.mesh_list.append(None)
        self.rebuild_panels()

    def delete_mesh(self, index):
        """
        Remove the mesh at the given index from both the dataset and the UI.
        """
        if 0 <= index < len(self.mesh_list):
            if self.mesh_list[index] is not None:
                ta.delete_read_object(self.dataset, self.mesh_list[index])
            del self.mesh_list[index]
            self.rebuild_panels()

    def change_class(
        self, change, index, select_widget, expansion_panel_content, doc_display
    ):
        """
        When a mesh type is selected, instantiate the corresponding class and update the dataset.
        Also rebuild the widget UI for the selected mesh.
        """
        if change and change.get("new"):
            new_class_name = change["new"]
            old_obj = self.mesh_list[index]
            new_obj = ta.trustify_gen_pyd.__dict__[new_class_name]()

            self.mesh_list[index] = new_obj

            if old_obj is None:
                ta.add_read_object(self.dataset, new_obj)
            else:
                obj_index = ta.get_entry_index(self.dataset, old_obj)
                self.dataset.entries[obj_index] = new_obj

            # Display widget fields for the new mesh class
            widgets = ObjectWidget.show_widget(
                new_obj,
                (type(new_obj), False),
                new_obj,
                [],
                [],
                True,
            )

            # Rebuild the content inside the panel
            expansion_panel_content.children = [select_widget, doc_display, widgets]
