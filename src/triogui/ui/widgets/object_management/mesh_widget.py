import ipyvuetify as v
import trioapi as ta
from ..object import ObjectWidget


class MeshWidget:
    def __init__(self, mesh_list, dataset):
        """
        Widget definition to manage list object for the dataset

        ----------
        Parameters

        mesh_list: list
            Every mesh of the dataset


        """

        self.mesh_list = mesh_list
        self.dataset = dataset
        self.mesh_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        self.btn_add_mesh = v.Btn(children="Add a mesh")
        self.btn_add_mesh.on_event("click", self.add_mesh)

        self.rebuild_panels()

        self.mesh_container = v.Container(
            children=[self.mesh_panels, self.btn_add_mesh]
        )

        self.content = [self.mesh_container]

    def rebuild_panels(self):
        self.mesh_panels.children = []

        for i, mesh in enumerate(self.mesh_list):
            new_select_type_mesh = v.Select(
                items=["Read_med", "Read_file", "Read_file_bin", "Read_tgrid"],
                label="Type of the mesh",
                v_model=None,
            )

            if mesh is not None:
                new_select_type_mesh.v_model = type(mesh).__name__
                panel_content = [
                    new_select_type_mesh,
                    ObjectWidget.show_widget(mesh, (type(mesh), False), mesh, [], []),
                ]
            else:
                panel_content = [new_select_type_mesh]

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

            expansion_panel_content = v.ExpansionPanelContent(children=panel_content)

            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[header_content]),
                    expansion_panel_content,
                ]
            )

            new_select_type_mesh.observe(
                lambda change,
                idx=i,
                select=new_select_type_mesh,
                content=expansion_panel_content: self.change_class(
                    change, idx, select, content
                ),
                "v_model",
            )

            self.mesh_panels.children = self.mesh_panels.children + [new_panel]

    def add_mesh(self, widget, event, data):
        self.mesh_list.append(None)
        self.rebuild_panels()

    def delete_mesh(self, index):
        if 0 <= index < len(self.mesh_list):
            if self.mesh_list[index] is not None:
                ta.delete_read_object(self.dataset, self.mesh_list[index])
            del self.mesh_list[index]

            self.rebuild_panels()

    def change_class(self, change, index, select_widget, expansion_panel_content):
        if change:
            old_value = self.mesh_list[index]
            self.mesh_list[index] = ta.trustify_gen_pyd.__dict__[change["new"]]()
            if old_value is None:
                ta.add_read_object(self.dataset, self.mesh_list[index])
            else:
                obj_index = ta.get_entry_index(self.dataset, old_value)
                self.dataset.entries[obj_index] = self.mesh_list[index]
            # Call show_widgets for the type selected (we instantiate the type and specify the tuple (type, is_list))
            widgets = ObjectWidget.show_widget(
                self.mesh_list[index],
                (type(self.mesh_list[index]), False),
                self.mesh_list[index],
                [],
                [],
                True,
            )
            expansion_panel_content.children = [select_widget, widgets]
