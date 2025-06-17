import ipyvuetify as v
import trioapi as ta


class FinalWidget:
    def __init__(self):
        """
        Widget definition for Final Page to write the dataset in a new data file

        This widget is composed by a text field to write the name of the file and a button to validate the choice.
        """

        self.dataset = None

        self.textfield = v.TextField(label="Name of the new data file", v_model=None)

        self.validate_button = v.Btn(children=["Validate"])
        self.main = [self.textfield, self.validate_button]
        self.validate_button.on_event("click", self.create_jdd)

    def create_jdd(self, widget, event, data):
        """
        Create a new datafile (named by the textfield) with the read object modified
        """
        ta.write_data(self.dataset, self.textfield.v_model)
