import ipyvuetify as v
from .object import ObjectWidget


class ListWidget:
    def __init__(
        self, current_object, expected_type, read_object, key_path, change_list
    ):
        """
        Creates a widget for editing lists of structured objects.

        Parameters
        ----------
        current_object : list
            The list of elements currently being edited.

        expected_type : type
            The type that each item in the list is expected to conform to.

        read_object : object
            The root object which is modified initially by the GUI containing this list.

        key_path : list
            The nested path to the list inside the read_object.

        change_list : list
            The list of change states for undo/redo support.

        This widget is composer by a panel for each items of the list. It is possible to add an element to the list
        and duplicate or delete each element. In the panel every field is displayed to modify the corresponding item
        """

        # UI container to hold the item panels
        self.container = v.Container(children=[])

        # Store input references
        self.current_object = current_object
        self.expected_type = expected_type
        self.read_object = read_object
        self.key_path = key_path
        self.change_list = change_list

        # Store references to action buttons
        self.delete_buttons = []
        self.duplicate_buttons = []

        # Button to add a new item to the list
        self.add_button = v.Btn(children=["Add a new item"])

        # Collapsible container that holds all item panels
        self.expand_panel = v.ExpansionPanels(children=[self.container])

        # Main content: panels + add button
        self.content = v.Content(children=[self.expand_panel, self.add_button])

        # Build the UI panels for all existing items
        self.build_panels(self.current_object)

    def build_panels(self, object_to_display):
        """
        Build the list of expansion panels, one per item in the list.

        Each item includes:
        - A header with its index and action buttons
        - A panel with editable fields rendered via ObjectWidget
        """
        # Reset UI
        self.container.children = []
        self.delete_buttons = []
        self.duplicate_buttons = []

        for i, item in enumerate(object_to_display):
            # Store current container state to append to
            current_container = self.container.children

            # Create delete button for item
            delete_button = v.Btn(
                icon=True,
                small=True,
                color="red",
                children=[v.Icon(children=["mdi-delete"])],
            )
            delete_button.kwargs = {"index": i}
            self.delete_buttons.append(delete_button)

            # Create duplicate button for item
            duplicate_button = v.Btn(
                icon=True,
                small=True,
                color="blue",
                children=[v.Icon(children=["mdi-content-copy"])],
            )
            duplicate_button.kwargs = {"index": i}
            self.duplicate_buttons.append(duplicate_button)

            # Wrap item content in expandable panel
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

            # Add the panel to the container
            self.container.children = current_container + [new_panel]
