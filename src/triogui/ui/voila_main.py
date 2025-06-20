import ipyvuetify as v
import triogui.ui.widgets as w  # noqa: F403
import trioapi as ta
import copy


def main():
    # Initialize prinpals widgets
    hw = w.HomeWidget()
    fw = w.FinalWidget()
    ow = w.ObjectWidget(
        ta.get_jdd("upwind_simplified").get("pb"),
        [ta.get_jdd("upwind_simplified").get("pb")],
    )
    # Create tabs for menu
    tab_widgets = [hw, fw, ow]
    tab_titles = ["Home", "Final", "pb"]

    tab = v.Tabs(
        v_model=0,
        center_active=True,
        fixed_tabs=True,
        slider_size=4,
        align_with_title=True,
        show_arrows=True,
        children=[v.Tab(children=[k]) for k in tab_titles],
    )

    content = v.Content(children=[])

    def tab_change(change):
        """
        Change the display according to the widget when the user is clicking on a new tab
        """
        widget = tab_widgets[tab.v_model]
        content.children = widget.main

    def get_jdd_btn(widget, event, data):
        """
        It creates the new widget and add the possibility of the tab for the object contained in the selectionned dataset
        """
        nonlocal tab_titles, tab_widgets
        dataset = ta.get_jdd(hw.select.v_model)
        read_objects = ta.get_read_objects(dataset)
        tab_titles = tab_titles[:2] + read_objects
        tab_widgets = tab_widgets[:2] + [
            w.ObjectWidget(dataset.get(i), [dataset.get(i)]) for i in read_objects
        ]
        tab.children = [v.Tab(children=[k]) for k in tab_titles]
        fw.dataset = dataset

    tab_change(None)
    tab.observe(tab_change, "v_model")
    hw.validate_button.on_event("click", get_jdd_btn)

    def setup_cancel_and_test_handlers(obj_widget):
        def cancel(widget, event, data):
            if len(obj_widget.change_list) > 1:
                obj_widget.change_list.pop()
                new_obj_widget = w.ObjectWidget(
                    copy.deepcopy(obj_widget.change_list[-1]), obj_widget.change_list
                )

                setup_cancel_and_test_handlers(new_obj_widget)  # recurse
                tab_widgets[2] = new_obj_widget
                content.children = new_obj_widget.main

        def test(widget, event, data):
            new_tab = w.TestWidget(obj_widget.change_list)
            tab_titles.append("a")
            tab_widgets.append(new_tab)
            tab.children = [v.Tab(children=[k]) for k in tab_titles]

        obj_widget.cancel_button.on_event("click", cancel)
        obj_widget.test_button.on_event("click", test)

    setup_cancel_and_test_handlers(ow)

    return v.App(
        children=[
            v.AppBar(
                children=[
                    tab,
                ],
                clipped_left=True,
                app=True,
                dark=True,
            ),
            content,
        ]
    )
