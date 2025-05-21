import ipyvuetify as v


class IntWidget:
    def __init__(self, initial_value):
        """
        Widget definition for Int Widget

        ----------
        Parameters

        initial_value: int
            The initial value of the dataset


        This widget is composed by a number input
        """

        self.number_input = v.TextField(
            label="Enter an int",
            type="number",
            outlined=True,
            v_model=initial_value,
        )

        self.content = v.Content(children=[self.number_input])
