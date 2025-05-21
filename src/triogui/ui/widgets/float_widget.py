import ipyvuetify as v


class FloatWidget:
    def __init__(self, initial_value):
        """
        Widget definition for Float Widget

        ----------
        Parameters

        initial_value: float
            The initial value of the dataset


        This widget is composed by a text field
        """

        self.float_field = v.TextField(
            label="Enter a float", type="number", clearable=True, v_model=initial_value
        )

        self.content = v.Content(children=[self.float_field])
