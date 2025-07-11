import ipyvuetify as v
import trioapi as ta
from ..object import ObjectWidget


class PartitionWidget:
    def __init__(self, partition_list, dataset):
        """
        Widget definition to manage list object for the dataset

        ----------
        Parameters

        partition_list: list
            Every partition of the dataset


        """

        self.partition_list = partition_list
        self.dataset = dataset

        self.partition_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        self.btn_add_partition = v.Btn(children="Add a partition")
        self.btn_add_partition.on_event("click", self.add_partition)

        self.rebuild_panels()

        self.partition_container = v.Container(
            children=[self.partition_panels, self.btn_add_partition]
        )

        self.content = [self.partition_container]

    def rebuild_panels(self):
        self.partition_panels.children = []
        for i, partition in enumerate(self.partition_list):
            btn_delete = v.Btn(
                children=[v.Icon(children="mdi-delete")],
                icon=True,
                color="red",
                small=True,
            )
            btn_delete.on_event(
                "click", lambda widget, event, data, idx=i: self.delete_partition(idx)
            )

            header_content = v.Row(
                children=[
                    v.Col(children=["Partition"], cols=10),
                    v.Col(children=[btn_delete], cols=2, class_="text-right"),
                ],
                no_gutters=True,
                align="center",
            )

            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[header_content]),
                    v.ExpansionPanelContent(
                        children=[
                            ObjectWidget.show_widget(
                                partition,
                                (ta.trustify_gen_pyd.Partition, False),
                                partition,
                                [],
                                [],
                            )
                        ]
                    ),
                ]
            )

            self.partition_panels.children = self.partition_panels.children + [
                new_panel
            ]

    def add_partition(self, widget, event, data):
        new_partition = ta.trustify_gen_pyd.Partition()
        self.partition_list.append(new_partition)
        ta.add_read_object(self.dataset, new_partition)
        self.rebuild_panels()

    def delete_partition(self, index):
        if 0 <= index < len(self.partition_list):
            if self.partition_list[index] is not None:
                ta.delete_read_object(self.dataset, self.partition_list[index])
            del self.partition_list[index]

            self.rebuild_panels()
