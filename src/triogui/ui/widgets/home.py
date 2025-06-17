import ipyvuetify as v
import os


class HomeWidget:
    def __init__(self):
        """
        Widget definition for Home Page

        This widget is composed by a dropdown to select the dataset we want to modify and a button to validate the choice.
        """

        dataset_list = [
            f[:-5] for f in os.listdir() if f.endswith(".data")
        ]  # Get list fo every datafile in the directory
        self.select = v.Select(
            items=dataset_list,
            label="Dataset",
            v_model=None,
        )

        self.validate_button = v.Btn(children=["Validate"])
        self.main = [self.select, self.validate_button]
