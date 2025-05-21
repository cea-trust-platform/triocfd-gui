import ipyvuetify as v


class BooleanWidget:
    def __init__(self, initial_value):
        """
        Widget definition for Boolean Widget

        ----------
        Parameters

        initial_value: int
            The initial value of the dataset


        This widget is composed by a switch
        """

        self.switch = v.Switch(label="", v_model=initial_value)

        self.content = v.Content(children=[self.switch])
