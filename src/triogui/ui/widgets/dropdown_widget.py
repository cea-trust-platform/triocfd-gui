import ipyvuetify as v


class DropdownWidget:
    def __init__(self, dropdown_list, initial_value):
        """
        Widget definition for Dropdown Widget

        ----------
        Parameters

        dropdown_list: list
            The list of every item of the dropdown

        initial_value: str
            The initial value of the dropdown

        This widget is composed by a dropdown
        """

        self.dropdown = v.Select(
            items=dropdown_list,
            v_model=initial_value,
            outlined=True,
            dense=True,
        )

        self.content = v.Content(children=[self.dropdown])
