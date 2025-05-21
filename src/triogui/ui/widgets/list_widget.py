import ipyvuetify as v
from .object import ObjectWidget


class ListWidget:
    def __init__(self, dict_type, value_list):
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

        self.dict_type = dict_type

        self.delete_buttons = []

        for i in range(len(value_list)):
            delete_button = v.Btn(children=["Delete this item"], color="red")
            delete_button.kwargs = {"index": len(self.delete_buttons)}
            delete_button.on_event("click", self.delete_item)
            self.delete_buttons.append(delete_button)
            new_panel = v.ExpansionPanel(
                children=[
                    v.ExpansionPanelHeader(children=[f"Item {i + 1}", delete_button]),
                    v.ExpansionPanelContent(
                        children=[ObjectWidget.show_widget(dict_type, value_list[i])]
                    ),
                ]
            )
            self.container.children.append(new_panel)

        self.add_button = v.Btn(children=["Add a new item"])
        self.expand_panel = v.ExpansionPanels(children=[self.container])

        self.content = v.Content(children=[self.expand_panel, self.add_button])
        self.add_button.on_event("click", self.display_widget)

    def display_widget(self, widget, event, data):
        current_container = self.container.children
        delete_button = v.Btn(children=["Delete this item"], color="red")
        delete_button.kwargs = {"index": len(self.delete_buttons)}
        delete_button.on_event("click", self.delete_item)
        self.delete_buttons.append(delete_button)
        new_panel = v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(
                    children=[
                        f"New Item {delete_button.kwargs['index'] + 1}",
                        delete_button,
                    ]
                ),
                v.ExpansionPanelContent(
                    children=[ObjectWidget.show_widget(self.dict_type, None)]
                ),
            ]
        )
        self.container.children = current_container + [new_panel]

    def delete_item(self, widget, event, data):
        current_container = self.container.children
        del current_container[widget.kwargs["index"]]
        del self.delete_buttons[widget.kwargs["index"]]
        for i, value in enumerate(self.delete_buttons):
            value.kwargs = {"index": i}
        self.container.children = current_container + [
            v.ExpansionPanel()
        ]  # Obliger de faire ça pour forcer l'affichage à s'update
        self.container.children.pop()  # Supprimer l'élément qu'on vient d'ajouter qui sert seulement à force l'affichage à s'update
