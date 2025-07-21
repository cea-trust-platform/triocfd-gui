import ipyvuetify as v
import trioapi as ta


class SchemeWidget:
    def __init__(self, sch_list, sch_callback, ds_callback, dataset):
        """
        Widget definition to manage list object for the dataset

        ----------
        Parameters

        sch_list: list
            Every scheme of the dataset
        """

        self.sch_callback = sch_callback
        self.sch_list = sch_list
        self.ds_callback = ds_callback
        self.dataset = dataset

        self.sch_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        self.sch_with_doc = []
        self.doc_dict = {}
        for sch in ta.get_subclass("Schema_temps_base"):
            sch_name = sch.__name__
            sch_doc = sch.__doc__
            self.sch_with_doc.append(
                {"text": f"{sch_name} - {sch_doc}", "value": sch_name}
            )
            self.doc_dict[sch_name] = sch_doc

        self.btn_add_sch = v.Btn(children="Add a scheme")
        self.btn_add_sch.on_event("click", self.add_sch)
        self.rebuild_panels()

        self.sch_container = v.Container(children=[self.sch_panels, self.btn_add_sch])

        self.content = [self.sch_container]

    def rebuild_panels(self):
        self.sch_panels.children = []
        for i, sch in enumerate(self.sch_list):
            new_name_sch = v.TextField(
                label="Name of the scheme",
                outlined=True,
                v_model=sch[0],
            )
            new_select_sch = v.Select(
                items=self.sch_with_doc,
                label="Type of the scheme",
                v_model=type(sch[1]).__name__,
            )

            doc_display = v.Alert(
                children=["Select an element to see its documentation"]
                if sch[1] is None
                else [self.doc_dict.get(new_select_sch.v_model)],
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
                "click", lambda widget, event, data, idx=i: self.delete_sch(idx)
            )

            header_content = v.Row(
                children=[
                    v.Col(children=["Scheme"], cols=10),
                    v.Col(children=[btn_delete], cols=2, class_="text-right"),
                ],
                no_gutters=True,
                align="center",
            )

            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[header_content]),
                    v.ExpansionPanelContent(
                        children=[new_name_sch, new_select_sch, doc_display]
                    ),
                ]
            )

            self.sch_panels.children = self.sch_panels.children + [new_panel]

            new_name_sch.observe(
                lambda change, idx=i, name=new_name_sch: self.update_menu(
                    change, idx, name, new_select_sch
                ),
                "v_model",
            )
            new_select_sch.observe(
                lambda change, idx=i, select=new_select_sch: self.update_menu(
                    change, idx, new_name_sch, select
                ),
                "v_model",
            )
            new_select_sch.observe(
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
            old_item = self.sch_list[index]
            already_created = None not in old_item
            if change["owner"] is name_widget:
                self.sch_list[index] = [change["new"], old_item[1]]
                self.sch_callback(index, 0, already_created, old_item[0], self.dataset)
            else:
                if old_item[1] is not None:
                    new_obj = ta.change_type_object(old_item[1], change["new"])
                else:
                    new_obj = getattr(ta.trustify_gen_pyd, change["new"])()
                self.sch_list[index] = [old_item[0], new_obj]
                self.sch_callback(index, 1, already_created, old_item[0], self.dataset)

    def add_sch(self, widget, event, data):
        self.sch_list.append([None, None])
        self.rebuild_panels()

    def delete_sch(self, index):
        if 0 <= index < len(self.sch_list):
            if self.sch_list[index][0] in self.dataset._declarations:
                ta.delete_object(self.dataset, self.sch_list[index][0])
            del self.sch_list[index]
            self.ds_callback(self.dataset)
            self.rebuild_panels()
