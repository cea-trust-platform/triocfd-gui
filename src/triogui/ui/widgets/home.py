import ipyvuetify as v
import ipywidgets as w
from ipyfilechooser import FileChooser
from importlib import resources
from .object import ObjectWidget
import trioapi as ta
import pyperclip
from .object_management import (
    problem_widget,
    scheme_widget,
    dimension_widget,
    domain_widget,
    discretization_widget,
    partition_widget,
    scatter_widget,
    mailler_widget,
    mesh_widget,
)


class HomeWidget:
    def __init__(self, ds_callback, pb_callback, pb_list, sch_list, sch_callback):
        """
        Widget definition for Home Page

        This widget is composed by a dropdown to select the dataset we want to modify and a button to validate the choice.
        """
        self.ds_callback = ds_callback
        self.pb_callback = pb_callback
        self.original_dataset = ta.trustify_gen_pyd.Dataset()
        self.original_dataset.entries.append(ta.trustify_gen_pyd.Dimension(dim=2))
        self.original_dataset.entries.append(ta.trustify_gen_pyd.Fin())
        self.dataset = self.original_dataset
        self.pb_list = pb_list
        self.sch_list = sch_list
        self.sch_callback = sch_callback

        # Get the package directory as a pathlib.Path object
        data_dir = resources.files("trioapi.data")

        self.dataset_list = [
            f.stem for f in data_dir.iterdir() if f.is_file() and f.suffix == ".data"
        ]  # Get list fo every datafile in the directory

        self.select = v.Select(
            items=self.dataset_list,
            label="Dataset",
            v_model=None,
        )
        self.upload = w.FileUpload(
            accept=".data",  # Accept only datafile
            multiple=False,
        )
        self.select.observe(self.update_widget, "v_model")
        self.update_widget(None)

        self.copy_btn = v.Btn(children=["Copy in clipboard"])

        self.copy_btn.on_event("click", self.copy_jdd)

        self.filefield = FileChooser(use_dir_icons=True, show_only_dirs=True)

        self.validate_button = v.Btn(children=["Validate"])

        self.filefield.register_callback(self.write_data_directory)

        self.panels = []

        # ----- DIMENSION -----

        self.dim_widget = dimension_widget.DimensionWidget(2, self.dataset)
        self.dim_content_container = v.Container(children=self.dim_widget.content)
        self.dim_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Dimension"]),
                v.ExpansionPanelContent(children=[self.dim_content_container]),
            ]
        )
        self.panels.append(self.dim_panel)

        # ----- DOMAINS -----

        self.dom_widget = domain_widget.DomainWidget([], self.dataset)
        self.domain_content_container = v.Container(children=self.dom_widget.content)
        self.domains_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Domains"]),
                v.ExpansionPanelContent(children=[self.domain_content_container]),
            ]
        )
        self.panels.append(self.domains_panel)

        # ----- MESH -----

        self.mesh_widget = mesh_widget.MeshWidget([], self.dataset)
        self.mesh_content_container = v.Container(children=self.mesh_widget.content)

        self.panels.append(
            v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Meshes"]),
                    v.ExpansionPanelContent(children=[self.mesh_content_container]),
                ]
            )
        )
        # ----- PARTITION -----
        self.partition_widget = partition_widget.PartitionWidget([], self.dataset)
        self.partition_content_container = v.Container(
            children=self.partition_widget.content
        )

        self.panels.append(
            v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Partitions"]),
                    v.ExpansionPanelContent(
                        children=[self.partition_content_container]
                    ),
                ]
            )
        )

        # ----- SCATTER -----

        self.scatter_widget = scatter_widget.ScatterWidget([], self.dataset)
        self.scatter_content_container = v.Container(
            children=self.scatter_widget.content
        )

        self.panels.append(
            v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Scatters"]),
                    v.ExpansionPanelContent(children=[self.scatter_content_container]),
                ]
            )
        )

        # ----- MAILLER -----

        self.mailler_widget = mailler_widget.MaillerWidget([], self.dataset)
        self.mailler_content_container = v.Container(
            children=self.mailler_widget.content
        )

        self.panels.append(
            v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Maillers"]),
                    v.ExpansionPanelContent(children=[self.mailler_content_container]),
                ]
            )
        )

        # ----- DISCRETIZATION -----
        self.dis_widget = discretization_widget.DiscretizationWidget([], self.dataset)
        self.dis_content_container = v.Container(children=self.dis_widget.content)

        self.panels.append(
            v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Discretizations"]),
                    v.ExpansionPanelContent(children=[self.dis_content_container]),
                ]
            )
        )

        # ----- PROBLEMS -----

        self.pb_widget = problem_widget.ProblemWidget(
            self.pb_list, callback=self.pb_callback, dataset=self.dataset
        )
        self.pb_content_container = v.Container(children=self.pb_widget.content)
        self.problems_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Problems"]),
                v.ExpansionPanelContent(children=[self.pb_content_container]),
            ]
        )
        self.panels.append(self.problems_panel)

        # ----- SCHEMES -----

        self.sch_widget = scheme_widget.SchemeWidget(
            self.sch_list, sch_callback=self.sch_callback, dataset=self.dataset
        )
        self.sch_content_container = v.Container(children=self.sch_widget.content)

        self.panels.append(
            v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Schemes"]),
                    v.ExpansionPanelContent(children=[self.sch_content_container]),
                ]
            )
        )

        # ----- ASSOCIATION -----

        # ----- SOLVE -----

        # ----- VALIDATE -----
        self.validate_btn = v.Btn(children="Create new dataset")

        # ----- MAIN LAYOUT -----
        self.main = [
            v.Container(
                children=[
                    # Existing dataset management
                    v.Card(
                        class_="ma-4 pa-4",
                        elevation=3,
                        children=[
                            v.CardTitle(
                                children=["Dataset Management"], class_="text-h5 mb-4"
                            ),
                            v.Divider(class_="mb-4"),
                            # Dataset provided selection
                            v.Row(
                                children=[
                                    v.Col(
                                        cols=4,
                                        children=[
                                            v.Html(
                                                tag="div",
                                                children=["Choose existing dataset:"],
                                                class_="text-subtitle-1 font-weight-medium",
                                            )
                                        ],
                                    ),
                                    v.Col(cols=8, children=[self.select]),
                                ],
                                align="center",
                                class_="mb-3",
                            ),
                            # Upload new dataset
                            v.Row(
                                children=[
                                    v.Col(
                                        cols=4,
                                        children=[
                                            v.Html(
                                                tag="div",
                                                children=["Upload new dataset:"],
                                                class_="text-subtitle-1 font-weight-medium",
                                            )
                                        ],
                                    ),
                                    v.Col(cols=8, children=[self.upload]),
                                ],
                                align="center",
                                class_="mb-4",
                            ),
                        ],
                    ),
                    # Dataset objects management
                    v.Card(
                        class_="ma-4 pa-4",
                        elevation=3,
                        children=[
                            v.CardTitle(
                                children=["Advanced Configuration"],
                                class_="text-h5 mb-4",
                            ),
                            v.Divider(class_="mb-4"),
                            v.ExpansionPanels(
                                children=self.panels, multiple=True, v_model=[]
                            ),
                        ],
                    ),
                    # Create file management
                    v.Card(
                        class_="ma-4 pa-4",
                        elevation=3,
                        children=[
                            v.CardTitle(
                                children=["File Management"], class_="text-h5 mb-4"
                            ),
                            v.Divider(class_="mb-4"),
                            v.Row(
                                children=[
                                    v.Col(
                                        cols=6,
                                        children=[
                                            v.Html(
                                                tag="div",
                                                children=["Select directory:"],
                                                class_="text-subtitle-1 font-weight-medium mb-2",
                                            ),
                                            self.filefield,
                                        ],
                                    ),
                                    v.Col(
                                        cols=6,
                                        children=[
                                            v.Html(
                                                tag="div",
                                                children=["Export options:"],
                                                class_="text-subtitle-1 font-weight-medium mb-2",
                                            ),
                                            self.copy_btn,
                                        ],
                                    ),
                                ]
                            ),
                        ],
                    ),
                ]
            )
        ]

    def update_widget(self, change):
        if change:
            selected_dataset = change["new"]
            if selected_dataset:
                self.dataset = ta.get_jdd(selected_dataset)

                # Dim management
                self.dim_widget = dimension_widget.DimensionWidget(
                    ta.get_dimension(self.dataset), self.dataset
                )
                self.dim_content_container.children = self.dim_widget.content

                # Dom management
                self.dom_widget = domain_widget.DomainWidget(
                    ta.get_domain(self.dataset), self.dataset
                )
                self.domain_content_container.children = self.dom_widget.content

                # Mesh management
                self.mesh_widget = mesh_widget.MeshWidget(
                    ta.get_mesh(self.dataset), self.dataset
                )
                self.mesh_content_container.children = self.mesh_widget.content

                # Partition
                self.partition_widget = partition_widget.PartitionWidget(
                    ta.get_partition(self.dataset), self.dataset
                )
                self.partition_content_container.children = (
                    self.partition_widget.content
                )

                # Scatter
                self.scatter_widget = scatter_widget.ScatterWidget(
                    ta.get_scatter(self.dataset), self.dataset
                )
                self.scatter_content_container.children = self.scatter_widget.content

                # Maillage
                self.mailler_widget = mailler_widget.MaillerWidget(
                    ta.get_maillage(self.dataset), self.dataset
                )
                self.mailler_content_container.children = self.mailler_widget.content

                # Discretization
                self.dis_widget = discretization_widget.DiscretizationWidget(
                    ta.get_dis(self.dataset), self.dataset
                )
                self.dis_content_container.children = self.dis_widget.content

                # Pb management
                self.pb_list.clear()
                self.pb_list.extend(ta.get_read_pb(self.dataset))
                self.pb_widget = problem_widget.ProblemWidget(
                    self.pb_list, callback=self.pb_callback, dataset=self.dataset
                )
                self.pb_content_container.children = self.pb_widget.content

                # Sch management
                self.sch_list.clear()
                self.sch_list.extend(ta.get_read_sch(self.dataset))
                self.sch_widget = scheme_widget.SchemeWidget(
                    self.sch_list, sch_callback=self.sch_callback, dataset=self.dataset
                )
                self.sch_content_container.children = self.sch_widget.content

                self.ds_callback(self.dataset)

    def copy_jdd(self, widget, event, data):
        """
        Copy the current dataset in the clipboard
        """
        newStream = self.dataset.toDatasetTokens()
        s = "".join(newStream)
        pyperclip.copy(s)

    def write_data_directory(self, chooser):
        ta.write_data(self.dataset, "XTESTX", chooser._selected_path)

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
