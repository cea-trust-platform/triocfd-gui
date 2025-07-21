import ipyvuetify as v
import trioapi as ta


class ProblemWidget:
    def __init__(self, pb_list, pb_callback, ds_callback, dataset):
        """
        Widget definition to manage problem object for the dataset

        ----------
        Parameters

        pb_list: list
            Every problem of the dataset


        This widget is composed by a switch
        """

        self.pb_callback = pb_callback
        self.pb_list = pb_list
        self.ds_callback = ds_callback
        self.dataset = dataset

        self.pb_with_doc = []
        self.doc_dict = {}
        for pb in ta.get_subclass("Pb_base"):
            pb_name = pb.__name__
            pb_doc = pb.__doc__
            self.pb_with_doc.append({"text": f"{pb_name} - {pb_doc}", "value": pb_name})
            self.doc_dict[pb_name] = pb_doc
        self.pb_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        self.btn_add_pb = v.Btn(children="Add a problem")
        self.btn_add_pb.on_event("click", self.add_pb)
        self.rebuild_panels()

        self.pb_container = v.Container(children=[self.pb_panels, self.btn_add_pb])

        self.content = [self.pb_container]

    def rebuild_panels(self):
        self.pb_panels.children = []
        for i, pb in enumerate(self.pb_list):
            new_name_pb = v.TextField(
                label="Name of the problem",
                outlined=True,
                v_model=pb[0],
            )

            new_select_pb = v.Select(
                items=self.pb_with_doc,
                label="Type of the problem",
                v_model=type(pb[1]).__name__,
            )

            doc_display = v.Alert(
                children=["Select an element to see its documentation"],
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
                "click", lambda widget, event, data, idx=i: self.delete_pb(idx)
            )

            header_content = v.Row(
                children=[
                    v.Col(children=["Problem"], cols=10),
                    v.Col(children=[btn_delete], cols=2, class_="text-right"),
                ],
                no_gutters=True,
                align="center",
            )

            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[header_content]),
                    v.ExpansionPanelContent(
                        children=[new_name_pb, new_select_pb, doc_display]
                    ),
                ]
            )

            self.pb_panels.children = self.pb_panels.children + [new_panel]

            new_name_pb.observe(
                lambda change, idx=i, name=new_name_pb: self.update_menu(
                    change, idx, name, new_select_pb
                ),
                "v_model",
            )
            new_select_pb.observe(
                lambda change, idx=i, select=new_select_pb: self.update_menu(
                    change, idx, new_name_pb, select
                ),
                "v_model",
            )
            new_select_pb.observe(
                lambda change, display=doc_display: self.update_doc(change, display),
                "v_model",
            )

    def update_doc(self, change, display_widget):
        """Updates the displayed documentation based on the selection."""
        if change and change.get("new"):
            selected_value = change["new"]
            doc_text = self.doc_dict.get(selected_value)
            display_widget.children = [doc_text]

    def update_menu(self, change, index, name_widget, select_widget):
        if change:
            old_item = self.pb_list[index]
            already_created = None not in old_item
            if change["owner"] is name_widget:
                self.pb_list[index] = [change["new"], old_item[1]]
                self.pb_callback(index, 0, already_created, old_item[0], self.dataset)
            else:
                if old_item[1] is not None:
                    new_obj = ta.change_type_object(old_item[1], change["new"])
                else:
                    new_obj = getattr(ta.trustify_gen_pyd, change["new"])()
                self.pb_list[index] = [old_item[0], new_obj]
                self.pb_callback(index, 1, already_created, old_item[0], self.dataset)

    def add_pb(self, widget, event, data):
        self.pb_list.append([None, None])
        self.rebuild_panels()

    def delete_pb(self, index):
        if 0 <= index < len(self.pb_list):
            if self.pb_list[index][0] in self.dataset._declarations:
                ta.delete_object(self.dataset, self.pb_list[index][0])
            del self.pb_list[index]
            self.ds_callback(self.dataset)
            self.rebuild_panels()
