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
        for i, dom in enumerate(self.dom_list):
            new_name_dom = v.TextField(
                label="Name of the domain",
                outlined=True,
                v_model=dom,
            )

            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=["Domain"]),
                    v.ExpansionPanelContent(children=[new_name_dom]),
                ]
            )

            self.dom_panels.children = self.dom_panels.children + [new_panel]

            new_name_dom.observe(
                lambda change, idx=i: self.update_domain(change, idx),
                "v_model",
            )

        self.dom_container = v.Container(children=[self.dom_panels, self.btn_add_dom])

        self.content = [self.dom_container]

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
        index = len(self.dom_list)
        self.dom_list.append(None)
        new_name_dom = v.TextField(
            label="Name of the domain",
            outlined=True,
            v_model=None,
        )

        new_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(children=["Domain"]),
                v.ExpansionPanelContent(children=[new_name_dom]),
            ]
        )
        self.dom_panels.children = self.dom_panels.children + [new_panel]
        # Append au dataset sur changement new_name_dom

        self.update_domain(None, index)
        new_name_dom.observe(
            lambda change, idx=index: self.update_domain(change, idx),
            "v_model",
        )
