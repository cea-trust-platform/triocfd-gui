import ipyvuetify as v
import trioapi as ta
from ..object import ObjectWidget


class MaillerWidget:
    def __init__(self, mailler_list, dataset):
        """
        Widget definition to manage mailles in the dataset.

        ----------
        Parameters

        mailler_list: list
            A list of mailles used in the dataset.

        dataset: Dataset
            The dataset being modified by the user.

        This widget provides an interface to add, display, and delete a Maille
        interactively. Each mailler is displayed in an expandable panel using the
        ObjectWidget rendering logic.
        """

        self.mailler_list = mailler_list
        self.dataset = dataset

        # Button to add a new Mailler
        self.btn_add_mailler = v.Btn(children="Add a maille")
        self.btn_add_mailler.on_event("click", self.add_mailler)

        # Expansion panel container for all Mailler entries
        self.mailler_panels = v.ExpansionPanels(
            v_model=[],
            multiple=True,
            children=[],
        )
        # Build the UI
        self.rebuild_panels()

        # Wrap into a container
        self.mailler_container = v.Container(
            children=[self.mailler_panels, self.btn_add_mailler]
        )

        self.content = [self.mailler_container]

    def rebuild_panels(self):
        """
        Refresh the list of displayed Mailler expansion panels.
        """
        self.mailler_panels.children = []

        for i, mailler in enumerate(self.mailler_list):
            # Delete button for the current mailler
            btn_delete = v.Btn(
                children=[v.Icon(children="mdi-delete")],
                icon=True,
                color="red",
                small=True,
            )
            btn_delete.on_event(
                "click", lambda widget, event, data, idx=i: self.delete_mailler(idx)
            )

            # Header row with label and delete action
            header_content = v.Row(
                children=[
                    v.Col(children=["Maille"], cols=10),
                    v.Col(children=[btn_delete], cols=2, class_="text-right"),
                ],
                no_gutters=True,
                align="center",
            )

            # Panel content uses ObjectWidget to render the mailler fields
            panel_content = ObjectWidget.show_widget(
                mailler,
                (ta.trustify_gen_pyd.Mailler, False),
                mailler,
                [],
                [],
            )

            # Create the panel for this maille
            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[header_content]),
                    v.ExpansionPanelContent(children=[panel_content]),
                ]
            )

            self.mailler_panels.children = self.mailler_panels.children + [new_panel]

    def add_mailler(self, widget, event, data):
        """
        Add a new mailler to the list and register it with the dataset.
        """
        new_maille = ta.trustify_gen_pyd.Mailler()
        self.mailler_list.append(new_maille)
        ta.add_read_object(self.dataset, new_maille)
        self.rebuild_panels()

    def delete_mailler(self, index):
        """
        Remove the mailler at the given index from the list and the dataset.
        """
        if 0 <= index < len(self.mailler_list):
            if self.mailler_list[index] is not None:
                ta.delete_read_object(self.dataset, self.mailler_list[index])

            del self.mailler_list[index]
            self.rebuild_panels()
