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
        for mesh in self.mesh_list:
            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Mesh"]),
                    v.ExpansionPanelContent(
                        children=[
                            ObjectWidget.show_widget(
                                mesh, (type(mesh), False), mesh, [], []
                            )
                        ]
                    ),
                ]
            )

            self.mesh_panels.children = self.mesh_panels.children + [new_panel]

        self.mesh_container = v.Container(
            children=[self.mesh_panels, self.btn_add_mesh]
        )

        self.content = [self.mesh_container]

    def add_mesh(self, widget, event, data):
        widget_index = len(self.mesh_list)

        self.mesh_list.append(None)
        new_select_type_mesh = v.Select(
            items=["Read_med", "Read_file", "Read_file_bin", "Read_tgrid"],
            label="Type of the mesh",
            v_model=None,
        )

        panel_content = v.ExpansionPanelContent(children=[new_select_type_mesh])

        new_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Mesh"]),
                panel_content,
            ]
        )

        self.mesh_panels.children = self.mesh_panels.children + [new_panel]

        def change_class(change):
            if change:
                old_value = self.mesh_list[widget_index]
                self.mesh_list[widget_index] = ta.trustify_gen_pyd.__dict__[
                    change["new"]
                ]()
                if old_value is None:
                    ta.add_read_object(self.dataset, self.mesh_list[widget_index])
                else:
                    obj_index = ta.get_entry_index(self.dataset, old_value)
                    self.dataset.entries[obj_index] = self.mesh_list[widget_index]
                # Call show_widgets for the type selected (we instantiate the type and specify the tuple (type, is_list))
                widgets = ObjectWidget.show_widget(
                    self.mesh_list[widget_index],
                    (type(self.mesh_list[widget_index]), False),
                    self.mesh_list[widget_index],
                    [],
                    [],
                )
                panel_content.children = [new_select_type_mesh, widgets]

        change_class(None)
        new_select_type_mesh.observe(change_class, "v_model")
