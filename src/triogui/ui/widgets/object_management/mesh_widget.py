import ipyvuetify as v
import trioapi as ta
from ..object import ObjectWidget


class MeshWidget:
    def __init__(self, mesh_list):
        """
        Widget definition to manage list object for the dataset

        ----------
        Parameters

        mesh_list: list
            Every mesh of the dataset


        """

        self.mesh_list = mesh_list

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
        # def update_menu(change):
        #    if change:
        #        old_item = self.mesh_list[index]
        #        already_created=(None not in old_item)
        #        if change['owner'] is new_name_mesh:
        #            self.mesh_list[index] = [change['new'], old_item[1]]
        #            self.mesh_callback(index, 0, already_created)
        #        else:
        #            self.mesh_list[index] = [old_item[0], getattr(ta.trustify_gen_pyd,change['new'])()]
        #            self.mesh_callback(index, 1, already_created)
        # update_menu(None)
        # new_name_mesh.observe(update_menu,"v_model")
        # new_select_mesh.observe(update_menu,"v_model")

        def change_class(change):
            if change:
                # Call show_widgets for the type selected (we instantiate the type and specify the tuple (type, is_list))
                widgets = ObjectWidget.show_widget(
                    ta.trustify_gen_pyd.__dict__[change["new"]](),
                    (ta.trustify_gen_pyd.__dict__[change["new"]], False),
                    ta.trustify_gen_pyd.__dict__[change["new"]](),
                    [],
                    [],
                )
                panel_content.children = [new_select_type_mesh, widgets]

        change_class(None)
        new_select_type_mesh.observe(change_class, "v_model")
