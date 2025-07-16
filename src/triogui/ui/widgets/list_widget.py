import ipyvuetify as v
from .object import ObjectWidget


class ListWidget:
    def __init__(
        self, current_object, expected_type, read_object, key_path, change_list
    ):
        """
        Widget definition for List Widget

        ----------
        Parameters

        dict_type: dict
            A dictionary containing the type of each item in the object within the list.

        value_list: list
            A list of every items of the list, each item respects the format : 1st index is the type of the item and the 2nd is a dict with the value of each attributes

        This widget is composed by every element to compose the list
        """
        self.container = v.Container(children=[])

        self.current_object = current_object
        self.expected_type = expected_type
        self.read_object = read_object
        self.key_path = key_path
        self.change_list = change_list
        self.delete_buttons = []
        self.duplicate_buttons = []

        self.add_button = v.Btn(children=["Add a new item"])
        self.expand_panel = v.ExpansionPanels(children=[self.container])

        self.content = v.Content(children=[self.expand_panel, self.add_button])

        self.build_panels(self.current_object)

    def build_panels(self, object_to_display):
        self.container.children = []
        self.delete_buttons = []
        self.duplicate_buttons = []
        for i, item in enumerate(object_to_display):
            current_container = self.container.children
            delete_button = v.Btn(
                icon=True,
                small=True,
                color="red",
                children=[v.Icon(children=["mdi-delete"])],
            )
            delete_button.kwargs = {"index": i}
            self.delete_buttons.append(delete_button)

            duplicate_button = v.Btn(
                icon=True,
                small=True,
                color="blue",
                children=[v.Icon(children=["mdi-content-copy"])],
            )
            duplicate_button.kwargs = {"index": i}
            self.duplicate_buttons.append(duplicate_button)

            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(
                        children=[
                            v.Row(
                                children=[
                                    v.Col(children=[f"Item {i + 1}"], cols=8),
                                    v.Col(children=[duplicate_button], cols=2),
                                    v.Col(children=[delete_button], cols=2),
                                ]
                            )
                        ]
                    ),
                    v.ExpansionPanelContent(
                        children=[
                            ObjectWidget.show_widget(
                                item,
                                (self.expected_type, False),
                                self.read_object,
                                self.key_path + [i],
                                self.change_list,
                            )
                        ]
                    ),
                ]
            )
            self.container.children = current_container + [new_panel]
