import trioapi as ta
import ipyvuetify as v


class AssociateWidget:
    def __init__(self, global_list, associate_list, dataset):
        self.global_list = global_list
        self.associate_list = associate_list
        self.dataset = dataset

        self.associate_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )
        self.btn_add_associate = v.Btn(children="Add an association")
        self.btn_add_associate.on_event("click", self.add_associate)

        self.rebuild_panels()

        self.associate_container = v.Container(
            children=[self.associate_panels, self.btn_add_associate]
        )
        self.content = [self.associate_container]

    def rebuild_panels(self):
        self.associate_panels.children = []
        for i, associate in enumerate(self.associate_list):
            select_1 = v.Select(
                items=self.global_list,
                label="First object to associate",
                v_model=associate[0],
            )

            select_2 = v.Select(
                items=self.global_list,
                label="Second object to associate",
                v_model=associate[1],
            )

            btn_delete = v.Btn(
                children=[v.Icon(children="mdi-delete")],
                icon=True,
                color="red",
                small=True,
            )
            btn_delete.on_event(
                "click", lambda widget, event, data, idx=i: self.delete_associate(idx)
            )

            header_content = v.Row(
                children=[
                    v.Col(children=["Association"], cols=10),
                    v.Col(children=[btn_delete], cols=2, class_="text-right"),
                ],
                no_gutters=True,
                align="center",
            )

            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[header_content]),
                    v.ExpansionPanelContent(children=[select_1, select_2]),
                ]
            )
            self.associate_panels.children = self.associate_panels.children + [
                new_panel
            ]

            select_1.observe(
                lambda change, idx=i: self.change_associate_dataset(change, idx, 1),
                "v_model",
            )

            select_2.observe(
                lambda change, idx=i: self.change_associate_dataset(change, idx, 2),
                "v_model",
            )

    def change_associate_dataset(self, change, index=None, select_type=None):
        old_item = self.associate_list[index]
        if select_type == 1:
            self.associate_list[index] = [change["new"], old_item[1]]
        else:
            self.associate_list[index] = [old_item[0], change["new"]]
        if None not in old_item:
            entry_index = ta.get_entry_index(
                self.dataset,
                ta.trustify_gen_pyd.Associate(objet_1=old_item[0], objet_2=old_item[1]),
            )
            self.dataset.entries[entry_index] = ta.trustify_gen_pyd.Associate(
                objet_1=self.associate_list[index][0],
                objet_2=self.associate_list[index][1],
            )
        elif None not in self.associate_list[index]:
            ta.add_read_object(
                self.dataset,
                ta.trustify_gen_pyd.Associate(
                    objet_1=self.associate_list[index][0],
                    objet_2=self.associate_list[index][1],
                ),
            )

    def add_associate(self, widget, event, data):
        self.associate_list.append([None, None])
        self.rebuild_panels()

    def delete_associate(self, index):
        if 0 <= index < len(self.associate_list):
            ta.delete_read_object(
                self.dataset,
                ta.trustify_gen_pyd.Associate(
                    objet_1=self.associate_list[index][0],
                    objet_2=self.associate_list[index][1],
                ),
            )
            del self.associate_list[index]

            self.rebuild_panels()
