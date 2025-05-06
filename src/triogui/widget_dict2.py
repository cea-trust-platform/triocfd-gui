import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium")

with app.setup:
    import trioapi as ta
    import typing
    import inspect
    import marimo as mo

    def create_widgets(key, value):
        if value is str:
            return mo.ui.text(label=key)
        if value is float:
            return mo.ui.text(label=key)
        if value is bool:
            return mo.ui.checkbox(label=key)
        if value is int:
            return mo.ui.number(label=key)
        if typing.get_origin(value) is typing.Literal:
            return mo.ui.dropdown(label=key, options=value.__args__)
        if type(value) is list:
            new_list = []
            for i, j in value[0].items():
                new_list.append(create_widgets(i, j))
            return new_list
        if typing.get_origin(value) is list:
            # TODO
            return None
        if inspect.isclass(value) and hasattr(ta, value.__name__):
            subclass_list = [i.__name__ for i in ta.get_subclass(value.__name__)]
            return mo.ui.dropdown(label=key, options=subclass_list)

    def show_widgets(dict_elem):
        iterator = iter(dict_elem.items())
        while True:
            try:
                key, value = next(iterator)
                if isinstance(value, dict):
                    show_widgets(value)
                else:
                    dict_elem[key] = create_widgets(key, value)
            except StopIteration:
                break
        return dict_elem

    def show_widgets_existing(dict_elem):
        iterator = iter(dict_elem.items())
        while True:
            try:
                key, value = next(iterator)
                if value is None:
                    pass
                elif isinstance(value, dict):
                    show_widgets_existing(value)
                else:
                    dict_elem[key] = create_widgets_existing(key, value)

            except StopIteration:
                break
        return dict_elem

    def create_widgets_existing(key, value_widget):
        if type(value_widget) is str:
            return mo.ui.text(label=key, value=value_widget)
        if type(value_widget) is float:
            return mo.ui.text(label=key, value=str(value_widget))
        if type(value_widget) is bool:
            return mo.ui.checkbox(label=key, value=value_widget)
        if type(value_widget) is int:
            return mo.ui.number(label=key, value=value_widget)
        if typing.get_origin(type(value_widget)) is typing.Literal:
            return mo.ui.dropdown(
                label=key, options=type(value_widget).__args__, value=value_widget
            )
        if type(value_widget) is list:
            new_list = []
            if isinstance(value_widget[0], dict):
                for i in value_widget:
                    new_list.append(show_widgets_existing(i))
            else:
                for i in value_widget:
                    new_list.append(create_widgets_existing(key, i))
            return new_list
        if typing.get_origin(type) is list:
            # TODO
            return None
        if inspect.isclass(type) and hasattr(ta, type.__name__):
            subclass_list = [i.__name__ for i in ta.get_subclass(value_widget.__name__)]
            return mo.ui.dropdown(label=key, options=subclass_list, value=value_widget)

    def final_widget(dict_ui_attr, dict_ui_obj):
        for key, value in dict_ui_obj.items():
            if not isinstance(dict_ui_attr, dict):
                pass
            elif value is None:
                dict_ui_obj[key] = dict_ui_attr[key]
            elif typing.get_origin(value) is typing.Literal:
                dict_ui_obj[key] = dict_ui_attr[key]
            elif isinstance(value, dict):
                final_widget(dict_ui_attr[key], dict_ui_obj[key])
        return dict_ui_obj


@app.function
def widgets_obj(obj):
    dict_type_attr = ta.get_successive_attributes(type(obj), {})
    dict_ui_attr = show_widgets(dict_type_attr)
    dict_obj = ta.obj_to_dict(obj)
    dict_ui_obj = show_widgets_existing(dict_obj)
    return final_widget(dict_ui_attr, dict_ui_obj)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
