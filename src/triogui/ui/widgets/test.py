import ipyvuetify as v


class TestWidget:
    def __init__(self, teststr):
        """
        Widget definition for Boolean Widget

        ----------
        Parameters

        initial_value: int
            The initial value of the dataset


        This widget is composed by a switch
        """

        self.content = v.Content(children=[str(teststr)])
        self.main = [str(teststr)]
