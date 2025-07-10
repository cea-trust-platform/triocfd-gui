import ipyvuetify as v
import triogui.ui.widgets as w  # noqa: F403
import trioapi as ta
from trustify.trust_parser import TRUSTParser, TRUSTStream
from .object import ObjectWidget


class MainApp:
    def __init__(self):
        # Initialize tab data structures
        self.tab_titles = ["Home"]
        self.tab_widgets = []  # Initialize as empty list first

        self.pb_list = []
        self.sch_list = []

        # Create the tab widget
        self.tab = v.Tabs(
            v_model=0,
            center_active=True,
            fixed_tabs=True,
            slider_size=4,
            align_with_title=True,
            show_arrows=True,
            children=[v.Tab(children=[k]) for k in self.tab_titles],
        )

        # Initialize principals widgets
        self.hw = w.HomeWidget(
            ds_callback=self.update_menu_dataset,
            pb_callback=self.update_menu_pb,
            pb_list=self.pb_list,
            sch_list=self.sch_list,
            sch_callback=self.update_menu_sch,
        )
        self.fw = w.FinalWidget()
        self.sw = w.StartZeroWidget()

        # Now populate the widgets list
        self.tab_widgets = [self.hw]

        self.content = v.Content(children=[])

        # Store the app as an instance variable instead of returning it
        self.app = v.App(
            children=[
                v.AppBar(
                    children=[
                        self.tab,
                    ],
                    clipped_left=True,
                    app=True,
                    dark=True,
                ),
                self.content,
            ]
        )

        def setup_cancel_and_test_handlers(index, obj_widget, identifier):
            def cancel(widget, event, data):
                if len(obj_widget.change_list) > 1:
                    obj_widget.change_list.pop()
                    restored = obj_widget.change_list[-1]
                    original = self.hw.dataset.get(identifier)

                    # Copy attributes
                    original.__dict__.clear()
                    original.__dict__.update(restored.__dict__)
                    new_obj_widget = w.ObjectWidget(original, obj_widget.change_list)

                    setup_cancel_and_test_handlers(
                        index, new_obj_widget, identifier
                    )  # recurse
                    self.tab_widgets[index] = new_obj_widget
                    self.content.children = new_obj_widget.main

            def test(widget, event, data):
                new_tab = w.TestWidget(obj_widget.change_list)
                self.tab_titles.append("a")
                self.tab_widgets.append(new_tab)
                self.tab.children = [v.Tab(children=[k]) for k in self.tab_titles]

            obj_widget.cancel_button.on_event("click", cancel)
            obj_widget.test_button.on_event("click", test)

        def get_jdd_btn(widget, event, data):
            """
            It creates the new widget and add the possibility of the tab for the object contained in the selectionned dataset
            """
            dataset = ta.get_jdd(self.hw.select.v_model)
            read_objects = ta.get_read_objects(dataset)
            self.tab_titles = self.tab_titles[:1] + read_objects
            widgets = [
                w.ObjectWidget(dataset.get(i), [dataset.get(i)]) for i in read_objects
            ]
            self.tab_widgets = self.tab_widgets[:1] + widgets
            self.tab.children = [v.Tab(children=[k]) for k in self.tab_titles]
            for index, widget in enumerate(widgets):
                setup_cancel_and_test_handlers(index + 1, widget, read_objects[index])
            self.hw.dataset = dataset

        self.tab_change(None)
        self.tab.observe(self.tab_change, "v_model")
        self.hw.validate_button.on_event("click", get_jdd_btn)

        def on_upload_change(inputs):
            data_ex = self.hw.upload.value[0].content.tobytes().decode("utf-8")

            tp = TRUSTParser()
            tp.tokenize(data_ex)
            stream = TRUSTStream(tp)
            dataset = ta.trustify_gen.Dataset_Parser.ReadFromTokens(stream)

            read_objects = ta.get_read_objects(dataset)
            self.tab_titles = self.tab_titles[:1] + read_objects
            widgets = [
                w.ObjectWidget(dataset.get(i), [dataset.get(i)]) for i in read_objects
            ]
            self.tab_widgets = self.tab_widgets[:1] + widgets
            self.tab.children = [v.Tab(children=[k]) for k in self.tab_titles]
            for index, widget in enumerate(widgets):
                setup_cancel_and_test_handlers(index + 1, widget, read_objects[index])
            self.hw.dataset = dataset

        self.hw.upload.observe(on_upload_change, names="value")

    def tab_change(self, change):
        """
        Change the display according to the widget when the user is clicking on a new tab
        """
        widget = self.tab_widgets[self.tab.v_model]
        self.content.children = widget.main

    def update_menu_pb(
        self, index, modified_object, already_created, original_identifier, dataset
    ):
        if already_created:
            if modified_object == 0:
                self.tab_titles[index + 1] = self.pb_list[index][0]
                ta.change_read_object(
                    dataset, original_identifier, "identifier", self.pb_list[index][0]
                )
            else:
                self.tab_widgets[index + 1] = ObjectWidget(
                    self.pb_list[index][1], [self.pb_list[index][1]]
                )
                ta.change_read_object(
                    dataset, original_identifier, "obj", self.pb_list[index][1]
                )

        elif None not in self.pb_list[index]:
            self.tab_titles.insert(index + 1, self.pb_list[index][0])
            self.tab_widgets.insert(
                index + 1,
                ObjectWidget(self.pb_list[index][1], [self.pb_list[index][1]]),
            )

            ta.add_object(dataset, self.pb_list[index][1], self.pb_list[index][0])

        self.tab.children = [v.Tab(children=[k]) for k in self.tab_titles]

    def update_menu_sch(
        self, index, modified_object, already_created, original_identifier, dataset
    ):
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

    def get_nbr_pb(self):
        nbr = 0
        for i in self.pb_list:
            if None not in i:
                nbr += 1
        return nbr

    def update_menu_dataset(self, dataset):
        read_objects = ta.get_read_objects(dataset)
        self.tab_titles = self.tab_titles[:1] + read_objects
        widgets = [
            w.ObjectWidget(dataset.get(i), [dataset.get(i)]) for i in read_objects
        ]
        self.tab_widgets = self.tab_widgets[:1] + widgets
        self.tab.children = [v.Tab(children=[k]) for k in self.tab_titles]

    def get_app(self):
        """Return the created app"""
        return self.app
