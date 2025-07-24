import ipyvuetify as v
import triogui.ui.widgets as w  # noqa: F403
import trioapi as ta

from .object import ObjectWidget


class MainApp:
    def __init__(self):
        """
        Main entry point of the GUI application.

        This class manages:
        - Tab navigation between different views
        - The Home screen
        - Display of Problems and Schemes
        - Object editing
        - Undo functionality for changes
        """
        # Initialize tab titles and content widgets
        self.tab_titles = ["Home"]
        self.tab_widgets = []  # One widget per tab

        # Lists for problems and schemes in the current dataset
        self.pb_list = []
        self.sch_list = []

        # Create the horizontal tab bar
        self.tab = v.Tabs(
            v_model=0,  # Active tab index
            center_active=True,
            fixed_tabs=True,
            slider_size=4,
            align_with_title=True,
            show_arrows=True,
            children=[v.Tab(children=[k]) for k in self.tab_titles],
        )

        # Create the HomeWidget and add it as the first (main) tab
        self.hw = w.HomeWidget(
            ds_callback=self.update_menu_dataset,
            pb_callback=self.update_menu_pb,
            pb_list=self.pb_list,
            sch_list=self.sch_list,
            sch_callback=self.update_menu_sch,
        )
        self.tab_widgets = [self.hw]

        # Create the main content area
        self.content = v.Content(children=[])

        # Full app layout
        self.app = v.App(
            children=[
                v.AppBar(children=[self.tab], clipped_left=True, app=True, dark=True),
                self.content,
            ]
        )

        # Set initial content
        self.tab_change(None)
        self.tab.observe(self.tab_change, "v_model")

    def tab_change(self, change):
        """
        Triggered when the user changes tabs.

        Displays the corresponding widget content for the selected tab.
        """
        widget = self.tab_widgets[self.tab.v_model]
        self.content.children = widget.main

    def update_menu_pb(
        self, index, modified_object, already_created, original_identifier, dataset
    ):
        """
        Updates the tab layout when a Problem is created or modified.

        Parameters
        ----------
        index : int
            Index of the problem in the list.

        modified_object : int
            0 if only the identifier was modified, 1 if the object type was modified.

        already_created : bool
            True if the problem already exists in the dataset.

        original_identifier : str
            Previous name of the problem (used for replacement).

        dataset : Dataset
            The dataset which is being modified.
        """
        if already_created:
            if modified_object == 0:
                # Identifier changed
                self.tab_titles[index + 1] = self.pb_list[index][0]
                ta.change_read_object(
                    dataset, original_identifier, "identifier", self.pb_list[index][0]
                )
            else:
                # Object type changed
                self.tab_widgets[index + 1] = ObjectWidget(
                    self.pb_list[index][1], [self.pb_list[index][1]]
                )
                ta.change_read_object(
                    dataset, original_identifier, "obj", self.pb_list[index][1]
                )
        elif None not in self.pb_list[index]:
            # New problem added
            self.tab_titles.insert(index + 1, self.pb_list[index][0])
            self.tab_widgets.insert(
                index + 1,
                ObjectWidget(self.pb_list[index][1], [self.pb_list[index][1]]),
            )
            ta.add_object(dataset, self.pb_list[index][1], self.pb_list[index][0])

        # Refresh the tab display
        self.tab.children = [v.Tab(children=[k]) for k in self.tab_titles]

        # Add undo functionality to each object widget
        for i, obj_widget in enumerate(self.tab_widgets[1:], 1):
            self.setup_cancel_buttons(i, obj_widget, dataset.get(self.tab_titles[i]))

    def update_menu_sch(
        self, index, modified_object, already_created, original_identifier, dataset
    ):
        """
        Updates the tab layout when a Scheme is created or modified.
        Logic is similar to `update_menu_pb`.

        Tabs are inserted after problem-related tabs.

        Parameters
        ----------
        index : int
            Index of the scheme in the list.

        modified_object : int
            0 for identifier change, 1 for type change.

        already_created : bool
            Whether the scheme was already part of the dataset.

        original_identifier : str
            The previous identifier of the scheme.

        dataset : Dataset
            The current dataset being modified.
        """
        tab_index = index + self.get_nbr_pb()
        if already_created:
            if modified_object == 0:
                self.tab_titles[tab_index + 1] = self.sch_list[index][0]
                ta.change_read_object(
                    dataset, original_identifier, "identifier", self.sch_list[index][0]
                )
            else:
                self.tab_widgets[tab_index + 1] = ObjectWidget(
                    self.sch_list[index][1], [self.sch_list[index][1]]
                )
                ta.change_read_object(
                    dataset, original_identifier, "obj", self.sch_list[index][1]
                )
        elif None not in self.sch_list[index]:
            self.tab_titles.insert(tab_index + 1, self.sch_list[index][0])
            self.tab_widgets.insert(
                tab_index + 1,
                ObjectWidget(self.sch_list[index][1], [self.sch_list[index][1]]),
            )
            ta.add_object(dataset, self.sch_list[index][1], self.sch_list[index][0])

        self.tab.children = [v.Tab(children=[k]) for k in self.tab_titles]

        for i, obj_widget in enumerate(self.tab_widgets[1:], 1):
            self.setup_cancel_buttons(i, obj_widget, dataset.get(self.tab_titles[i]))

    def get_nbr_pb(self):
        """
        Returns the number of valid (non-empty) problems in the pb_list.
        """
        nbr = 0
        for i in self.pb_list:
            if None not in i:
                nbr += 1
        return nbr

    def update_menu_dataset(self, dataset):
        """
        Updates the full menu (tabs and widgets) based on a newly loaded dataset.

        Parameters
        ----------
        dataset : Dataset
            The new dataset to load into the UI.
        """
        read_objects = [pb[0] for pb in ta.get_read_pb(dataset)] + [
            sch[0] for sch in ta.get_read_sch(dataset)
        ]
        self.tab_titles = self.tab_titles[:1] + read_objects

        # Create ObjectWidgets for each problem and scheme
        widgets = [
            w.ObjectWidget(dataset.get(i), [dataset.get(i)]) for i in read_objects
        ]
        self.tab_widgets = self.tab_widgets[:1] + widgets

        # Update the tab bar
        self.tab.children = [v.Tab(children=[k]) for k in self.tab_titles]

        # Add cancel buttons for each editable object
        for i, obj_widget in enumerate(self.tab_widgets[1:], 1):
            self.setup_cancel_buttons(i, obj_widget, dataset.get(self.tab_titles[i]))

    def setup_cancel_buttons(self, index, obj_widget, original):
        """
        Adds undo behavior to a given ObjectWidget via the Cancel button.

        Parameters
        ----------
        index : int
            Tab index for the widget.

        obj_widget : ObjectWidget
            The current editable object widget.

        original : object
            The original object instance tied to the dataset.
        """

        def cancel(widget, event, data):
            # Undo the last change if there's a history
            if len(obj_widget.change_list) > 1:
                obj_widget.change_list.pop()
                restored = obj_widget.change_list[-1]

                # Replace object attributes to revert state
                original.__dict__.clear()
                original.__dict__.update(restored.__dict__)

                # Recreate the widget with restored state
                new_obj_widget = w.ObjectWidget(original, obj_widget.change_list)
                self.setup_cancel_buttons(index, new_obj_widget, original)
                self.tab_widgets[index] = new_obj_widget
                self.content.children = new_obj_widget.main

        obj_widget.cancel_button.on_event("click", cancel)

    def get_app(self):
        """Return the created app"""
        return self.app
