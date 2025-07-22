import ipyvuetify as v


class StrWidget:
    def __init__(self, initial_value):
        """
        Widget definition for Str Widget

        ----------
        Parameters

        initial_value: str
            The initial value of the str

        This widget is composed by a text field

        """

        self.text_str = v.TextField(
            label="Enter a caracter chain",
            v_model=initial_value,
            outlined=True,
            auto_grow=False,
            style="height: 20px; font-size: 8px;",
        )

        self.content = v.Content(children=[self.text_str])
