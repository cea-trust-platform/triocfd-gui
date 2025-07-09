import ipyvuetify as v
import trioapi as ta
from ..object import ObjectWidget


class PartitionWidget:
    def __init__(self, partition_list):
        """
        Widget definition to manage list object for the dataset

        ----------
        Parameters

        partition_list: list
            Every partition of the dataset


        """

        self.partition_list = partition_list

        self.partition_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        self.btn_add_partition = v.Btn(children="Add a partition")
        self.btn_add_partition.on_event("click", self.add_partition)
        for partition in self.partition_list:
            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Partition"]),
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

        self.partition_container = v.Container(
            children=[self.partition_panels, self.btn_add_partition]
        )

        self.content = [self.partition_container]

    def add_partition(self, widget, event, data):
        new_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Partition"]),
                v.ExpansionPanelContent(
                    children=[
                        ObjectWidget.show_widget(
                            None, (ta.trustify_gen_pyd.Partition, False), None, [], []
                        )
                    ]
                ),
            ]
        )

        self.partition_panels.children = self.partition_panels.children + [new_panel]
        # def update_menu(change):
        #    if change:
        #        old_item = self.partition_list[index]
        #        already_created=(None not in old_item)
        #        if change['owner'] is new_name_partition:
        #            self.partition_list[index] = [change['new'], old_item[1]]
        #            self.partition_callback(index, 0, already_created)
        #        else:
        #            self.partition_list[index] = [old_item[0], getattr(ta.trustify_gen_pyd,change['new'])()]
        #            self.partition_callback(index, 1, already_created)
        # update_menu(None)
        # new_name_partition.observe(update_menu,"v_model")
        # new_select_partition.observe(update_menu,"v_model")
