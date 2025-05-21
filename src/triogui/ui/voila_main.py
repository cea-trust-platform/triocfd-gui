import ipyvuetify as v
import triogui.ui.widgets as w  # noqa: F403
import trioapi as ta


def main():
    hw = w.HomeWidget()
    fw = w.FinalWidget()
    dataset = ta.get_jdd("upwind_simplified")
    pb = dataset.get("pb")
    ow = w.ObjectWidget(pb)

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
        widget = tab_widgets[tab.v_model]
        content.children = widget.main

    def get_jdd_btn(widget, event, data):
        nonlocal tab_titles, tab_widgets
        # dataset=ta.get_jdd(hw.select.v_model)
        # read_objects=ta.get_read_objects(dataset)
        # tab_titles+=read_objects
        # tab_widgets+=[ObjectWidget(dataset.get(i)) for i in read_objects]
        # tab.children=[v.Tab(children=[k]) for k in tab_titles]

    tab_change(None)
    tab.observe(tab_change, "v_model")
    hw.validate_button.on_event("click", get_jdd_btn)

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
