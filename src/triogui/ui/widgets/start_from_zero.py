import ipyvuetify as v
from .object import ObjectWidget
import trioapi as ta


class StartZeroWidget:
    def __init__(self):
        self.panels = []

        # ----- DIMENSION -----
        self.dimension = v.TextField(
            label="Enter the wished dimension (int)",
            type="number",
            outlined=True,
            v_model=2,
        )

        self.panels.append(
            v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Dimension"]),
                    v.ExpansionPanelContent(children=[self.dimension]),
                ]
            )
        )

        # ----- DOMAINS AND MESHES -----
        self.domain_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        self.domains = v.TextField(
            label="Name of the domain",
            type="number",
            outlined=True,
            v_model=None,
        )

        self.mesh = v.Select(
            items=["Read_file", "Read_file_bin", "Read_med"],
            label="Type of the mesh",
            v_model=None,
        )

        self.btn_add_domain = v.Btn(children=["Add a domain"])
        self.btn_add_domain.on_event("click", self.add_domain)

        self.domain_container = v.Container(
            children=[self.domain_panels, self.btn_add_domain]
        )

        self.panels.append(
            v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Domains"]),
                    v.ExpansionPanelContent(children=[self.domain_container]),
                ]
            )
        )

        # ----- PROBLEMS -----
        self.pb_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        self.select_pb = v.Select(
            items=[
                str(i.__name__)
                for i in ta.get_subclass(ta.trustify_gen_pyd.Pb_base.__name__)
            ],
            label="Type of the problem",
            v_model=None,
        )

        self.btn_add_pb = v.Btn(children="Add a problem")
        self.btn_add_pb.on_event("click", self.add_pb)

        self.pb_container = v.Container(children=[self.pb_panels, self.btn_add_pb])

        self.panels.append(
            v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Problems"]),
                    v.ExpansionPanelContent(children=[self.pb_container]),
                ]
            )
        )

        # ----- SCHEMES -----
        self.sch_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        self.select_sch = v.Select(
            items=[
                str(i.__name__)
                for i in ta.get_subclass(ta.trustify_gen_pyd.Schema_temps_base.__name__)
            ],
            label="Type of the scheme",
            v_model=None,
        )

        self.btn_add_sch = v.Btn(children="Add a scheme")
        self.btn_add_sch.on_event("click", self.add_sch)

        self.sch_container = v.Container(children=[self.sch_panels, self.btn_add_sch])

        # self.panels.append(
        #    v.ExpansionPanel(
        #        children=[
        #            v.ExpansionPanelHeader(children=["Schemes"]),
        #            v.ExpansionPanelContent(children=[self.sch_container]),
        #        ]
        #    )
        # )

        self.panels.append(
            v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Associated mesh"]),
                    v.ExpansionPanelContent(
                        children=[
                            ObjectWidget.show_widget(
                                ta.trustify_gen_pyd.Read_file(),
                                (ta.trustify_gen_pyd.Read_file, False),
                                ta.trustify_gen_pyd.Read_file(),
                                [],
                                [],
                            )
                        ]
                    ),
                ]
            )
        )

        # ----- VALIDATE -----
        self.validate_btn = v.Btn(children="Create new dataset")

        # ----- MAIN LAYOUT -----
        self.main = [
            v.ExpansionPanels(children=self.panels, multiple=True, v_model=[]),
            self.validate_btn,
        ]

    def add_domain(self, widget, event, data):
        new_domain = v.TextField(
            label="Name of the domain",
            type="number",
            outlined=True,
            v_model=None,
        )
        add_mesh_btn = v.Btn(children=["Add a mesh to this domain"])

        new_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Domain"]),
                v.ExpansionPanelContent(children=[new_domain, add_mesh_btn]),
            ]
        )
        self.domain_panels.children = self.domain_panels.children + [new_panel]

        add_mesh_btn.on_event("click", self.add_mesh)

    def add_pb(self, widget, event, data):
        new_name_pb = v.TextField(
            label="Name of the problem",
            type="number",
            outlined=True,
            v_model=None,
        )
        new_select_pb = v.Select(
            items=[
                str(i.__name__)
                for i in ta.get_subclass(ta.trustify_gen_pyd.Pb_base.__name__)
            ],
            label="Type of the problem",
            v_model=None,
        )

        new_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Problem"]),
                v.ExpansionPanelContent(children=[new_name_pb, new_select_pb]),
            ]
        )
        self.pb_panels.children = self.pb_panels.children + [new_panel]

    def add_sch(self, widget, event, data):
        new_name_sch = v.TextField(
            label="Name of the scheme",
            type="number",
            outlined=True,
            v_model=None,
        )

        new_select_sch = v.Select(
            items=[
                str(i.__name__)
                for i in ta.get_subclass(ta.trustify_gen_pyd.Schema_temps_base.__name__)
            ],
            label="Type of the scheme",
            v_model=None,
        )

        new_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Scheme"]),
                v.ExpansionPanelContent(children=[new_name_sch, new_select_sch]),
            ]
        )
        self.sch_panels.children = self.sch_panels.children + [new_panel]

    def add_mesh(self, widget, event, data):
        new_mesh = v.Select(
            items=["Read_file", "Read_file_bin", "Read_med"],
            label="Type of the mesh",
            v_model=None,
        )
        new_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Associated mesh"]),
                v.ExpansionPanelContent(children=[new_mesh]),
            ]
        )
        self.domain_panels.children = self.domain_panels.children + [new_panel]
        new_mesh.on_event("blur", self.get_mesh_widget)

    def get_mesh_widget(self, widget, event, data):
        new_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Associated mesh"]),
                v.ExpansionPanelContent(
                    children=[
                        ObjectWidget.show_widget(
                            getattr(ta.trustify_gen_pyd, widget.v_model)(),
                            (getattr(ta.trustify_gen_pyd, widget.v_model), False),
                            getattr(ta.trustify_gen_pyd, widget.v_model)(),
                            [],
                            [],
                        )
                    ]
                ),
            ]
        )
        self.domain_panels.children = self.domain_panels.children + [new_panel]
