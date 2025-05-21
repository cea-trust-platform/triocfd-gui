import ipyvuetify as v


class FinalWidget:
    def __init__(self):
        """
        Widget definition for Final Page to write the dataset in a new data file

        This widget is composed by a text field to write the name of the file and a button to validate the choice.
        """
        self.textfield = v.TextField(label="Name of the new data file")

        self.validate_button = v.Btn(children=["Validate"])
        self.main = [self.textfield, self.validate_button]
