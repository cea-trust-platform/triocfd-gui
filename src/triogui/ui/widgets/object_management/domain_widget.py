import ipyvuetify as v
import trioapi as ta


class DomainWidget:
    def __init__(self, dom_list, dataset):
        """
        Widget definition to manage list object for the dataset

        ----------
        Parameters

        dom_list: list
            Every domain of the dataset
        """

        self.dom_list = dom_list
        self.dataset = dataset

        self.dom_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        self.btn_add_dom = v.Btn(children="Add a domain")
        self.btn_add_dom.on_event("click", self.add_domain)
        self.rebuild_panels()

        self.dom_container = v.Container(children=[self.dom_panels, self.btn_add_dom])

        self.content = [self.dom_container]

    def rebuild_panels(self):
        self.dom_panels.children = []
        for i, dom in enumerate(self.dom_list):
            new_name_dom = v.TextField(
                label="Name of the domain",
                outlined=True,
                v_model=dom,
            )

            btn_delete = v.Btn(
                children=[v.Icon(children="mdi-delete")],
                icon=True,
                color="red",
                small=True,
            )
            btn_delete.on_event(
                "click", lambda widget, event, data, idx=i: self.delete_dom(idx)
            )

            header_content = v.Row(
                children=[
                    v.Col(children=["Domain"], cols=10),
                    v.Col(children=[btn_delete], cols=2, class_="text-right"),
                ],
                no_gutters=True,
                align="center",
            )

            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[header_content]),
                    v.ExpansionPanelContent(children=[new_name_dom]),
                ]
            )

            self.dom_panels.children = self.dom_panels.children + [new_panel]

            new_name_dom.observe(
                lambda change, idx=i: self.update_domain(change, idx),
                "v_model",
            )

    def update_domain(self, change, index):
        if change:
            old_dom = self.dom_list[index]
            self.dom_list[index] = change["new"]
            already_created = old_dom is not None
            if already_created:
                ta.change_declaration_object(
                    self.dataset, old_dom, "identifier", self.dom_list[index]
                )
            else:
                ta.add_declaration_object(
                    self.dataset, ta.trustify_gen_pyd.Domaine(), self.dom_list[index]
                )

    def add_domain(self, widget, event, data):
        self.dom_list.append(None)
        self.rebuild_panels()

    def delete_dom(self, index):
        if 0 <= index < len(self.dom_list):
            if self.dom_list[index] in self.dataset._declarations:
                ta.delete_declaration_object(self.dataset, self.dom_list[index])
            del self.dom_list[index]

            self.rebuild_panels()
