import ipyvuetify as v
import trioapi as ta


class DiscretizationWidget:
    def __init__(self, dis_list, dataset):
        """
        Widget definition to manage list object for the dataset

        ----------
        Parameters

        dis_list: list
            Every discretization of the dataset


        """

        self.dis_list = dis_list
        self.dataset = dataset

        self.dis_with_doc = []
        self.doc_dict = {}
        for dis in ta.get_subclass("Discretisation_base"):
            dis_name = dis.__name__
            dis_doc = dis.__doc__
            self.dis_with_doc.append(
                {"text": f"{dis_name} - {dis_doc}", "value": dis_name}
            )
            self.doc_dict[dis_name] = dis_doc

        self.dis_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        self.btn_add_dis = v.Btn(children="Add a discretization")
        self.btn_add_dis.on_event("click", self.add_dis)

        self.rebuild_panels()

        self.dis_container = v.Container(children=[self.dis_panels, self.btn_add_dis])

        self.content = [self.dis_container]

    def rebuild_panels(self):
        self.dis_panels.children = []
        for i, dis in enumerate(self.dis_list):
            new_name_dis = v.TextField(
                label="Name of the discretization",
                outlined=True,
                v_model=dis[0],
            )
            new_select_dis = v.Select(
                items=self.dis_with_doc,
                label="Type of the discretization",
                v_model=dis[1].__name__ if dis[1] is not None else None,
            )

            doc_display = v.Alert(
                children=["Select an element to see its documentation"]
                if dis[1] is None
                else [self.doc_dict.get(new_select_dis.v_model)],
                type="info",
                outlined=True,
                class_="text-body-2 pa-2 mt-2",
                style_="white-space: pre-wrap;",
            )

            btn_delete = v.Btn(
                children=[v.Icon(children="mdi-delete")],
                icon=True,
                color="red",
                small=True,
            )
            btn_delete.on_event(
                "click", lambda widget, event, data, idx=i: self.delete_dis(idx)
            )

            # switch = v.Switch(label="Add parameters to this discretization", v_model=False)
            # switch.index=i
            # switch.on_event("change", self.change_read_dis)
            #
            header_content = v.Row(
                children=[
                    v.Col(children=["Discretization"], cols=10),
                    v.Col(children=[btn_delete], cols=2, class_="text-right"),
                ],
                no_gutters=True,
                align="center",
            )

            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[header_content]),
                    v.ExpansionPanelContent(
                        children=[new_name_dis, new_select_dis, doc_display]
                    ),
                ]
            )

            self.dis_panels.children = self.dis_panels.children + [new_panel]

            new_name_dis.observe(
                lambda change, idx=i, name=new_name_dis: self.update_dataset(
                    change, idx, name, new_select_dis
                ),
                "v_model",
            )
            new_select_dis.observe(
                lambda change, idx=i, select=new_select_dis: self.update_dataset(
                    change, idx, new_name_dis, select
                ),
                "v_model",
            )
            new_select_dis.observe(
                lambda change, display=doc_display: self.update_doc(change, display),
                "v_model",
            )

    def update_doc(self, change, display_widget):
        """Updates the displayed documentation based on the selection."""
        if change and change.get("new"):
            selected_value = change["new"]
            doc_text = self.doc_dict.get(selected_value)
            display_widget.children = [doc_text]

    def update_dataset(self, change, index, name_widget, select_widget):
        if change:
            old_item = self.dis_list[index]
            already_created = None not in old_item
            if already_created:
                if change["owner"] is name_widget:
                    self.dis_list[index] = [change["new"], old_item[1]]
                    ta.change_declaration_object(
                        self.dataset, old_item[0], "identifier", self.dis_list[index][0]
                    )
                else:
                    new_type = getattr(ta.trustify_gen_pyd, change["new"])
                    self.dis_list[index] = [old_item[0], new_type]
                    ta.change_declaration_object(
                        self.dataset, old_item[0], "ze_type", self.dis_list[index][1]
                    )
            else:
                if change["owner"] is name_widget:
                    self.dis_list[index] = [change["new"], old_item[1]]
                else:
                    new_type = getattr(ta.trustify_gen_pyd, change["new"])
                    self.dis_list[index] = [old_item[0], new_type]
                if None not in self.dis_list[index]:
                    ta.add_declaration_object(
                        self.dataset, self.dis_list[index][1](), self.dis_list[index][0]
                    )

    def add_dis(self, widget, event, data):
        self.dis_list.append([None, None])
        self.rebuild_panels()

    def delete_dis(self, index):
        if 0 <= index < len(self.dis_list):
            if self.dis_list[index][0] in self.dataset._declarations:
                ta.delete_declaration_object(self.dataset, self.dis_list[index][0])
            del self.dis_list[index]

            self.rebuild_panels()

    # def change_read_dis(self, widget, event, data):
    #    new_value = widget.v_model
    #    identifier = self.dis_list[widget.index][0]
    #    class_name=self.dis_list[widget.index][1]
    #    if new_value:
    #        ta.add_read_object(self.dataset, ta.trustify_gen_pyd.Read(identifier=identifier, obj=class_name()))
    #        entry_index=ta.get_entry_index(self.dataset,ta.trustify_gen_pyd.Read(identifier=identifier, obj=class_name()))
    #        self.dataset._declarations[identifier][1]=entry_index
    #    else:
    #        ta.delete_read_object(
    #            self.dataset, self.dataset.get(identifier)
    #        )
