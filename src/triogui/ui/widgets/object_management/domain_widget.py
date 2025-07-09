import ipyvuetify as v


class DomainWidget:
    def __init__(self, dom_list):
        """
        Widget definition to manage list object for the dataset

        ----------
        Parameters

        dom_list: list
            Every domain of the dataset
        """

        self.dom_list = dom_list

        self.dom_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )

        self.btn_add_dom = v.Btn(children="Add a domain")
        self.btn_add_dom.on_event("click", self.add_domain)
        for dom in self.dom_list:
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

        self.dom_container = v.Container(children=[self.dom_panels, self.btn_add_dom])

        self.content = [self.dom_container]

    def add_domain(self, widget, event, data):
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
