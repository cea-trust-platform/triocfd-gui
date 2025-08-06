import ipyvuetify as v
import ipywidgets as w
from ipyfilechooser import FileChooser
from importlib import resources
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
    solve_widget,
    associate_widget,
    discretize_widget,
    coupled_problem_widget,
    ecriture_lecture_special_widget,
)
from trustify.trust_parser import TRUSTParser, TRUSTStream


class HomeWidget:
    def __init__(self, ds_callback, pb_callback, pb_list, sch_list, sch_callback):
        """
        Widget definition for the Home Page interface.

        ----------
        Parameters

        ds_callback: Callable
            Callback function used to notify a dataset update.

        pb_callback: Callable
            Callback for problem management.

        pb_list: list
            List to hold the problems defined in the current dataset.

        sch_list: list
            List to hold the schemes defined in the current dataset.

        sch_callback: Callable
            Callback for scheme updates.

        This widget provides a full interface for managing a dataset,
        including dimensions, domains, meshes, partitions, scatters, maillers,
        discretizations, problems, schemes, associations, discretization, and solving.
        """
        # Store callbacks and lists
        self.ds_callback = ds_callback
        self.pb_callback = pb_callback
        self.pb_list = pb_list
        self.sch_list = sch_list
        self.sch_callback = sch_callback

        # Initialize an empty dataset
        self.original_dataset = ta.trustify_gen_pyd.Dataset()
        self.original_dataset.entries.append(ta.trustify_gen_pyd.Dimension(dim=2))
        self.original_dataset.entries.append(ta.trustify_gen_pyd.Fin())
        self.dataset = self.original_dataset

        # Get already solved problems from the dataset
        self.solve_list = ta.get_solved_problems(self.dataset)

        # Load dataset file list from internal data folder
        data_dir = resources.files("trioapi.data")
        self.dataset_list = ["Create from scratch"] + [
            f.stem for f in data_dir.iterdir() if f.is_file() and f.suffix == ".data"
        ]

        # Dataset selection dropdown
        self.select = v.Select(
            items=self.dataset_list,
            label="Dataset",
            v_model="Create from scratch",
        )
        self.select.observe(self.on_select_change, "v_model")
        self.on_select_change(None)

        # File upload widget for loading a dataset file
        self.upload = w.FileUpload(
            accept=".data",
            multiple=False,
        )
        self.upload.observe(self.on_upload_change, names="value")

        # Button to copy the current dataset to clipboard
        self.copy_btn = v.Btn(children=["Copy in clipboard"])
        self.copy_btn.on_event("click", self.copy_jdd)

        # File chooser and filename field for exporting the dataset
        self.filefield = FileChooser(use_dir_icons=True, show_only_dirs=True)
        self.file_name = v.TextField(
            label="File name",
            v_model=None,
            outlined=True,
            dense=True,
            hide_details=True,
            single_line=True,
            class_="mb-2",
        )

        # Button to confirm saving the dataset
        self.validate_button = v.Btn(children=["Validate"])
        self.filefield.register_callback(self.write_data_directory)

        # List of expandable panels for each dataset component
        self.panels = []

        # ----- Create and add widget panels for each dataset component -----

        # Dimension panel
        self.dim_widget = dimension_widget.DimensionWidget(2, self.dataset)
        self.dim_content_container = v.Container(children=self.dim_widget.content)
        self.dim_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Dimension"]),
                v.ExpansionPanelContent(children=[self.dim_content_container]),
            ]
        )
        self.panels.append(self.dim_panel)

        # Domains panel
        self.dom_widget = domain_widget.DomainWidget([], self.dataset)
        self.domain_content_container = v.Container(children=self.dom_widget.content)
        self.domains_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Domains"]),
                v.ExpansionPanelContent(children=[self.domain_content_container]),
            ]
        )
        self.panels.append(self.domains_panel)

        # Mesh panel
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

        # Partition panel
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

        # Scatter panel
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

        # Mailler panel
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

        # Discretization panel
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

        # Problems panel
        self.pb_widget = problem_widget.ProblemWidget(
            self.pb_list,
            pb_callback=self.pb_callback,
            ds_callback=self.ds_callback,
            dataset=self.dataset,
        )
        self.pb_content_container = v.Container(children=self.pb_widget.content)
        self.problems_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Problems"]),
                v.ExpansionPanelContent(children=[self.pb_content_container]),
            ]
        )
        self.panels.append(self.problems_panel)

        # Schemes panel
        self.sch_widget = scheme_widget.SchemeWidget(
            self.sch_list,
            sch_callback=self.sch_callback,
            ds_callback=self.ds_callback,
            dataset=self.dataset,
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

        # Associations panel
        self.associate_widget = associate_widget.AssociateWidget(
            [], dataset=self.dataset
        )
        self.associate_content_container = v.Container(
            children=self.associate_widget.content
        )
        self.panels.append(
            v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Associations"]),
                    v.ExpansionPanelContent(
                        children=[self.associate_content_container]
                    ),
                ]
            )
        )

        # Discretize panel
        self.discretize_widget = discretize_widget.DiscretizeWidget(
            [], dataset=self.dataset
        )
        self.discretize_content_container = v.Container(
            children=self.discretize_widget.content
        )
        self.panels.append(
            v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Discretize"]),
                    v.ExpansionPanelContent(
                        children=[self.discretize_content_container]
                    ),
                ]
            )
        )

        # Solve panel
        self.solve_widget = solve_widget.SolveWidget(
            self.solve_list, dataset=self.dataset
        )
        self.solve_content_container = v.Container(children=self.solve_widget.content)
        self.panels.append(
            v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Solves"]),
                    v.ExpansionPanelContent(children=[self.solve_content_container]),
                ]
            )
        )

        # Coupled Problems panel
        self.coupled_problem_widget = coupled_problem_widget.CoupledProblemWidget(
            [], dataset=self.dataset
        )
        self.coupled_problem_content_container = v.Container(
            children=self.coupled_problem_widget.content
        )
        self.panels.append(
            v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Coupled problems"]),
                    v.ExpansionPanelContent(
                        children=[self.coupled_problem_content_container]
                    ),
                ]
            )
        )

        # Ecriture lecture special panel
        self.ecriture_lecture_special_widget = (
            ecriture_lecture_special_widget.EcritureLectureSpecialWidget(
                dataset=self.dataset
            )
        )
        self.ecriture_lecture_special_container = v.Container(
            children=self.ecriture_lecture_special_widget.content
        )
        self.panels.append(
            v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(
                        children=[
                            "Choose to write or not to write a .xyz file on the disk at the end of the calculation. (Ecriturelecturespecial keyword)"
                        ]
                    ),
                    v.ExpansionPanelContent(
                        children=[self.ecriture_lecture_special_container]
                    ),
                ]
            )
        )

        filefield_container = v.Container(
            children=[self.filefield], style_="max-width: 100%; overflow-x: auto;"
        )

        # Main layout container, grouping all the UI elements
        self.main = [
            v.Container(
                children=[
                    # Dataset management section
                    v.Card(
                        class_="ma-4 pa-4",
                        elevation=3,
                        children=[
                            v.CardTitle(
                                children=["Dataset Management"], class_="text-h5 mb-4"
                            ),
                            v.Divider(class_="mb-4"),
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
                    # Advanced dataset configuration
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
                    # File management section
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
                                            self.file_name,
                                            filefield_container,
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

    def on_select_change(self, change):
        """
        Triggered when the user selects a different dataset from the dropdown.

        If 'Create from scratch' is selected, the widget reverts to the initial dataset.
        Otherwise, the selected dataset is loaded from the internal storage via the Trio API.
        The interface is then updated to reflect the contents of the new dataset.
        """
        if change:
            selected_dataset = change["new"]
            if selected_dataset == "Create from scratch":
                self.dataset = self.original_dataset
            else:
                self.dataset = ta.get_jdd(selected_dataset)
            self.update_dataset()

    def on_upload_change(self, inputs):
        """
        Triggered when a new dataset file is uploaded via the FileUpload widget.

        The uploaded file is parsed using the TRUSTParser and TRUSTStream classes,
        then used to create a new dataset object. The widget is refreshed accordingly.
        """
        data_ex = self.upload.value[0].content.tobytes().decode("utf-8")
        tp = TRUSTParser()
        tp.tokenize(data_ex)
        stream = TRUSTStream(tp)
        dataset = ta.trustify_gen.Dataset_Parser.ReadFromTokens(stream)
        self.dataset = dataset
        self.update_dataset()

    def update_dataset(self):
        """
        Rebuilds all child widgets and UI panels based on the current dataset.

        This method is responsible for:
        - Re-initializing all sub-widgets with updated dataset content
        - Refreshing problem and scheme lists
        - Updating containers used by the expansion panels
        - Triggering the main dataset callback
        """
        # Dimension management
        self.dim_widget = dimension_widget.DimensionWidget(
            ta.get_dimension(self.dataset), self.dataset
        )
        self.dim_content_container.children = self.dim_widget.content

        # Domain management
        self.dom_widget = domain_widget.DomainWidget(
            ta.get_domain(self.dataset), self.dataset
        )
        self.domain_content_container.children = self.dom_widget.content

        # Mesh management
        self.mesh_widget = mesh_widget.MeshWidget(
            ta.get_mesh(self.dataset), self.dataset
        )
        self.mesh_content_container.children = self.mesh_widget.content

        # Partition management
        self.partition_widget = partition_widget.PartitionWidget(
            ta.get_partition(self.dataset), self.dataset
        )
        self.partition_content_container.children = self.partition_widget.content

        # Scatter management
        self.scatter_widget = scatter_widget.ScatterWidget(
            ta.get_scatter(self.dataset), self.dataset
        )
        self.scatter_content_container.children = self.scatter_widget.content

        # Mailler (mesh generator) management
        self.mailler_widget = mailler_widget.MaillerWidget(
            ta.get_maillage(self.dataset), self.dataset
        )
        self.mailler_content_container.children = self.mailler_widget.content

        # Discretization management
        self.dis_widget = discretization_widget.DiscretizationWidget(
            ta.get_dis(self.dataset), self.dataset
        )
        self.dis_content_container.children = self.dis_widget.content

        # Problem management
        self.pb_list.clear()
        self.pb_list.extend(ta.get_read_pb(self.dataset))
        self.pb_widget = problem_widget.ProblemWidget(
            self.pb_list,
            pb_callback=self.pb_callback,
            ds_callback=self.ds_callback,
            dataset=self.dataset,
        )
        self.pb_content_container.children = self.pb_widget.content

        # Scheme management
        self.sch_list.clear()
        self.sch_list.extend(ta.get_read_sch(self.dataset))
        self.sch_widget = scheme_widget.SchemeWidget(
            self.sch_list,
            sch_callback=self.sch_callback,
            ds_callback=self.ds_callback,
            dataset=self.dataset,
        )
        self.sch_content_container.children = self.sch_widget.content

        # Association management
        self.associate_widget = associate_widget.AssociateWidget(
            ta.get_associations(self.dataset),
            dataset=self.dataset,
        )
        self.associate_content_container.children = self.associate_widget.content

        # Discretize management
        self.discretize_widget = discretize_widget.DiscretizeWidget(
            ta.get_discretize(self.dataset),
            dataset=self.dataset,
        )
        self.discretize_content_container.children = self.discretize_widget.content

        # Solve management
        self.solve_list.clear()
        self.solve_list.extend(ta.get_solved_problems(self.dataset))
        self.solve_widget = solve_widget.SolveWidget(
            self.solve_list, dataset=self.dataset
        )
        self.solve_content_container.children = self.solve_widget.content

        # Coupled problem management
        self.coupled_problem_widget = coupled_problem_widget.CoupledProblemWidget(
            ta.get_coupled_problems(self.dataset), dataset=self.dataset
        )
        self.coupled_problem_content_container.children = (
            self.coupled_problem_widget.content
        )

        # EcritureLectureSpecial object management (to manage if xyz file is written or not)
        self.ecriture_lecture_special_widget = (
            ecriture_lecture_special_widget.EcritureLectureSpecialWidget(
                dataset=self.dataset
            )
        )
        self.ecriture_lecture_special_container.children = (
            self.ecriture_lecture_special_widget.content
        )

        # Notify parent component of the dataset change
        self.ds_callback(self.dataset)

    def copy_jdd(self, widget, event, data):
        """
        Copies the current dataset to the system clipboard.
        """
        newStream = self.dataset.toDatasetTokens()
        s = "".join(newStream)
        pyperclip.copy(s)

    def write_data_directory(self, chooser):
        """
        Writes the current dataset to the selected directory and filename.
        """
        ta.write_data(self.dataset, self.file_name.v_model, chooser._selected_path)
