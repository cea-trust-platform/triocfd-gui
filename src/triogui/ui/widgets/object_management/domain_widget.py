import ipyvuetify as v
import trioapi as ta


class DomainWidget:
    def __init__(self, dom_list, dataset):
        """
        Widget definition to manage domain declarations in the dataset.

        ----------
        Parameters

        dom_list: list
            A list of domain identifiers associated with the dataset.

        dataset: Dataset
            The dataset being edited by the user.

        This widget displays each domain as an expansion panel with an editable name field
        and a delete button. Users can add, modify, or remove domains, and changes are updated
        in the dataset.
        """

        # Store references to the domain list and dataset
        self.dom_list = dom_list
        self.dataset = dataset

        # Add button to insert a new domain
        self.btn_add_dom = v.Btn(children="Add a domain")
        self.btn_add_dom.on_event("click", self.add_domain)

        # Create the container for domain expansion panels
        self.dom_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )
        # Build the initial panel UI
        self.rebuild_panels()

        # Wrap everything into a container
        self.dom_container = v.Container(children=[self.dom_panels, self.btn_add_dom])
        self.content = [self.dom_container]

    def rebuild_panels(self):
        """
        Refresh the expansion panels based on the current list of domains.
        """
        self.dom_panels.children = []

        # Iterate through each domain in the list
        for i, dom in enumerate(self.dom_list):
            # Text field to edit the domain identifier
            new_name_dom = v.TextField(
                label="Name of the domain",
                outlined=True,
                v_model=dom,
            )

            # Delete button
            btn_delete = v.Btn(
                children=[v.Icon(children="mdi-delete")],
                icon=True,
                color="red",
                small=True,
            )
            btn_delete.on_event(
                "click", lambda widget, event, data, idx=i: self.delete_dom(idx)
            )

            # Header row with label and delete action
            header_content = v.Row(
                children=[
                    v.Col(children=["Domain"], cols=10),
                    v.Col(children=[btn_delete], cols=2, class_="text-right"),
                ],
                no_gutters=True,
                align="center",
            )

            # Build expansion panel for this domain
            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[header_content]),
                    v.ExpansionPanelContent(children=[new_name_dom]),
                ]
            )

            # Append panel to the list
            self.dom_panels.children = self.dom_panels.children + [new_panel]

            # Observe changes in the name field to sync with the dataset
            new_name_dom.observe(
                lambda change, idx=i: self.update_domain(change, idx),
                "v_model",
            )

    def update_domain(self, change, index):
        """
        Called when a domain name is changed.

        Updates the internal list and modifies the dataset accordingly.
        """
        if change:
            old_dom = self.dom_list[index]
            self.dom_list[index] = change["new"]
            already_created = old_dom is not None

            # If domain already existed, update its identifier
            if already_created:
                ta.change_declaration_object(
                    self.dataset,
                    old_dom,
                    "identifier",
                    self.dom_list[index],
                )
            # Otherwise, create a new domain object in the dataset
            else:
                ta.add_declaration_object(
                    self.dataset,
                    ta.trustify_gen_pyd.Domaine(),
                    self.dom_list[index],
                )

    def add_domain(self, widget, event, data):
        """
        Add a new (empty) domain entry and refresh the UI.
        """
        self.dom_list.append(None)
        self.rebuild_panels()

    def delete_dom(self, index):
        """
        Delete a domain from the internal list and remove it from the dataset.
        """
        if 0 <= index < len(self.dom_list):
            # Remove from dataset if it was declared
            if self.dom_list[index] in self.dataset._declarations:
                ta.delete_declaration_object(self.dataset, self.dom_list[index])

            # Remove from internal list
            del self.dom_list[index]

            # Refresh UI
            self.rebuild_panels()
